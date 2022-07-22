# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    approve_limit_1 = fields.Monetary()
    approve_limit_2 = fields.Monetary()
    #daily_limit_1 = fields.Monetary()
    #daily_limit_2 = fields.Monetary()