# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    barcode_ids = fields.One2many(
        comodel_name="product.barcode",
        inverse_name="product_tmpl_id",
        string="Barcodes",
    )