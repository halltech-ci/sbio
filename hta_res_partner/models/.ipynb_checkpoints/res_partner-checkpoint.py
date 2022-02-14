# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)