# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    
    def action_generate_serial(self):
        self.ensure_one()
        
        self.lot_producing_id = self.env['stock.production.lot'].create({
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'name': self.env['stock.production.lot']._get_next_serial(self.company_id, self.product_id) or self.env['ir.sequence'].next_by_code(self.product_id.lot_sequence_id.code) or self.env['ir.sequence'].next_by_code('stock.lot.serial'),
            #'name': self.env['stock.production.lot']._get_next_serial(self.company_id, self.product_id) or self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        })
        if self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids:
            self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids.lot_id = self.lot_producing_id
        if self.product_id.tracking == 'serial':
            self._set_qty_producing()