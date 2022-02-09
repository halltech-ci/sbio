# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    lot_prefixe = fields.Char()
    manufacturing_unit = fields.Many2one('uom.uom', help="Unite de mesure fabrication.")
    
