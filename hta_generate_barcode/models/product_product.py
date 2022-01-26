# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "barcode.generate.mixin"]
