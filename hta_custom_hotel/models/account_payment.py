# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"


    reservation_id = fields.Many2one("hotel.reservation")