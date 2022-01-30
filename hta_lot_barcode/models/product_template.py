# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    lot_prefixe = fields.Char()
    conditioning_unit = fields.Many2one('uom.uom', help="Unite de mesure de conditionnement.")
    
class ProductProduct(models.Model):
    _inherit = "product.product"
    
    conditioning_qty = fields.Float(string="Qte de conditionnement")
    
    
    