# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hta_stock(models.Model):
    _inherit = 'stock.picking'

    receipt_user = fields.Many2one('res.users', string="Utlisateur Receip")
