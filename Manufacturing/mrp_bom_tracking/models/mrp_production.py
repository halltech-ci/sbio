# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    date_planned_start = fields.Datetime(tracking=True)
    product_id = fields.Many2one(tracking=True)
    product_tmpl_id = fields.Many2one(tracking=True)
    product_qty = fields.Float(tracking=True)
    bom_id = fields.Many2one(tracking=True)
    #type = fields.Selection(tracking=True)

    def write(self, values):
        move_raw_ids = {}
        if "move_raw_ids" in values:
            for bom in self:
                del_lines = []
                for line in values["move_raw_ids"]:
                    if line[0] == 2:
                        del_lines.append(line[1])
                if del_lines:
                    bom.message_post_with_view(
                        "mrp_bom_tracking.track_mrp_template",
                        values={
                            "lines": self.env["stock.move"].browse(del_lines),
                            "mode": "Removed",
                        },
                        subtype_id=self.env.ref("mail.mt_note").id,
                    )
                move_raw_ids[bom.id] = bom.move_raw_ids
        res = super(MrpProduction, self).write(values)
        if "move_raw_ids" in values:
            for bom in self:
                new_lines = bom.move_raw_ids - move_raw_ids[bom.id]
                if new_lines:
                    bom.message_post_with_view(
                        "mrp_bom_tracking.track_mrp_template",
                        values={"lines": new_lines, "mode": "New"},
                        subtype_id=self.env.ref("mail.mt_note").id,
                    )
        return res


class MrpStockMove(models.Model):
    _inherit = "stock.move"

    def write(self, values):
        if "product_id" in values:
            for bom in self.mapped("raw_material_production_id"):
                lines = self.filtered(lambda l: l.raw_material_production_id == bom)
                product_id = values.get("product_id")
                if product_id:
                    product_id = self.env["product.product"].browse(product_id)
                product_id = product_id or lines.product_id
                if lines:
                    bom.message_post_with_view(
                        "mrp_bom_tracking.track_mrp_line_template",
                        values={"lines": lines, "product_id": product_id},
                        subtype_id=self.env.ref("mail.mt_note").id,
                    )
        elif "product_uom_qty" in values or "product_uom_id" in values:
            for bom in self.mapped("raw_material_production_id"):
                lines = self.filtered(lambda l: l.raw_material_production_id == bom)
                if lines:
                    product_uom_qty = values.get("product_uom_qty") or lines.product_uom_qty
                    quantity_done = values.get("quantity_done")
                    #product_uom_id = product_uom_id or lines.product_uom_id
                    bom.message_post_with_view(
                        "mrp_bom_tracking.track_mrp_line_template",
                        values={
                            "lines": lines,
                            "product_uom_qty": product_uom_qty,
                            "quantity_done": quantity_done,
                        },
                        subtype_id=self.env.ref("mail.mt_note").id,
                    )
        return super(MrpStockMove, self).write(values)
