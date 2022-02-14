# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCompany(models.Model):
    _inherit = 'res.partner'

    company_delivery = fields.Boolean()
    person_delivery = fields.Boolean()
    
    pos_orders = fields.One2many('pos.order', 'delivery_person', string='Commandes',readonly=True, copy=False)
    
    
    

