# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    
    lot_number = fields.Char(string="N° Lot", compute="_compute_lot_number")
    
    