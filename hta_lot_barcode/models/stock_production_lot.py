# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    
    lot_number = fields.Char(string="N° Lot", 
                             #compute="_compute_lot_number",
                            )
        
    def _get_lot_number(self, date, company, product):
        if product.tracking == "lot" and not product.template_id.prefixe :
            if product.use_expiration_date and not product.expiration_time:
                raise ValidationError(_('The combination of serial number and product must be unique across a company.\nFollowing combination contains duplicates:\n'))
            prefixe = product.template_id.prefixe
            scheduled_date 
        
    
    @api.model
    def _get_next_serial(self, company, product):
        """Return the next serial number to be attributed to the product."""
        if product.tracking == "serial":
            last_serial = self.env['stock.production.lot'].search(
                [('company_id', '=', company.id), ('product_id', '=', product.id)],
                limit=1, order='id DESC')
            if last_serial:
                return self.env['stock.production.lot'].generate_lot_names(last_serial.name, 2)[1]
        if product.tracking == "lot" and not product.template_id.prefixe :
            if product.use_expiration_date and not product.expiration_time:
                raise ValidationError(_('The combination of serial number and product must be unique across a company.\nFollowing combination contains duplicates:\n'))
            prefixe = product.template_id.prefixe
            scheduled_date 
            
        return False
    