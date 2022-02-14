# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCompany(models.Model):
    _inherit = 'res.partner'

    company_delivery = fields.Boolean()
    person_delivery = fields.Boolean()
    
    
    

