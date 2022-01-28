# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    lot_prefixe = fields.Char(string="Prefixe")
    