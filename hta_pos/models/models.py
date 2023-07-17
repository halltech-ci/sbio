# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Notice(models.Model):
    _name = 'product.notice'
    _inherit = "mail.thread"
    _description = 'Notice'

    name = fields.Char(required=True, tracking=True,string="Produit")
    description = fields.Html("Description", help="Mettre les produits du kit",tracking=True)
    price = fields.Float(tracking=True,string="Prix")
    notice = fields.Text(required=True, tracking=True,string="Notice")


