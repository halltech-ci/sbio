# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryAgent(models.Model):
    _name = 'delivery.agent'
    _inherit = "mail.thread"
    _description = 'Livreur'

    name = fields.Char(required=True, tracking=True, string="Nom du livreur")
    phone_number = fields.Char()
    partner_id = fields.Many2one("res.partner")


