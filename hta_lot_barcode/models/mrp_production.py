# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    def action_generate_serial(self):
        self.ensure_one()
        prefixe = self.product_tmpl_id.barcode
        if product_tmpl_id.tracking not in ['lot']:
            raise ValidationError(_('You must check tracking lot in product template'))
        if product_tmpl_id.use_expiration_date:
            expiration_time = product_tmpl_id.expiration_time
            schedule_date = self.product_tmpl_id.lot_prefixe
        self.lot_producing_id = self.env['stock.production.lot'].create({
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'name': self.env['stock.production.lot']._get_next_serial(self.company_id, self.product_id) or self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        })
        if self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids:
            self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids.lot_id = self.lot_producing_id
        if self.product_id.tracking == 'serial':
            self._set_qty_producing()
    