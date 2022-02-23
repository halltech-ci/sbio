from odoo import models, fields, api

class HtaPos(models.Model):
    _inherit = 'pos.order'
    

    customer_Phone = fields.Char()
    delivery_phone = fields.Char()
   

    @api.onchange("partner_id")
    def _onchange_customer_Phone(self):
        for rec in self:
            if rec.partner_id:
                rec.customer_Phone = rec.partner_id.phone
                
    @api.onchange("delivery_person")
    def _onchange_delivery_phone(self):
        for rec in self:
            if rec.delivery_person:
                rec.delivery_phone = rec.delivery_person.phone
