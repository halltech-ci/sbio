# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id and self.product_id.product_tmpl_id.lot_sequence_id:
            self.name = self.product_id.product_tmpl_id.lot_sequence_id._next()
            
    @api.model
    def _get_next_serial(self, company, product):
        """Return the next serial number to be attributed to the product."""
        #if product.tracking in ["serial", "lot"]:
        if product.tracking == "serial":
            last_serial = self.env['stock.production.lot'].search(
                [('company_id', '=', company.id), ('product_id', '=', product.id)],
                limit=1, order='id DESC')
            if last_serial:
                return self.env['stock.production.lot'].generate_lot_names(last_serial.name, 2)[1]
        return False
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for lot_vals in vals_list:
            if "name" not in lot_vals:
                product = self.env["product.product"].browse(lot_vals["product_id"])
                if product and product.product_tmpl_id.lot_sequence_id:
                    lot_vals["name"] = product.product_tmpl_id.lot_sequence_id._next()
        return super(ProductionLot, self).create(vals_list)