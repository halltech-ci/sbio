# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    pos_reference = fields.Char(related="pos_order_id.pos_reference", string="Référence")


