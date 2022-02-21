# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HtaPos(models.Model):
    _inherit = 'pos.order'
    

    delivery_person = fields.Many2one(
        comodel_name="res.partner",
        string="Livreur",
    )

    date_delivery = fields.Datetime()
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


# class AssignPos(models.Model):
#     _name = 'assign.commands'
#     _description = "Assign Commande to Delivery Person"
#     _inherit = ["mail.thread", "mail.activity.mixin"]
#     _order = "id desc"

#     delivery_person = fields.Many2one(
#         comodel_name="res.partner",
#         string="Delivery Person",
#     )
#     purchase_lines = fields.Many2many(
#         comodel_name="pos.order",
#         string="Commands",
#         readonly=True,
#         copy=False,
#     )
#     date_delivery = fields.Datetime()


