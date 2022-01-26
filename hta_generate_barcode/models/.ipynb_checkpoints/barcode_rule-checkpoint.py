# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BarcodeRule(models.Model):
    _inherit = "barcode.rule"

    generate_model = fields.Selection(selection_add=[("product.product", "Products")])