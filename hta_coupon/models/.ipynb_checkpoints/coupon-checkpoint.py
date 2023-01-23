# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hta_coupon(models.Model):
    _inherit = 'coupon.coupon'

    partner_Phone = fields.Char("Telephone",related='partner_id.phone', store=True)