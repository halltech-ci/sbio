# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)