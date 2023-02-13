# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rapport_notice(models.Model):
    _name = 'rapport_notice.rapport_notice'
    _description = 'rapport_notice.rapport_notice'

    name = fields.Char(string="Nom")
    notice = fields.Text(string="Notice")
    # product = fields.Many2one("product.product",string="Product")

    # @api.depends('value')
    # def _value_pc(self):
    #     for record in self:
    #         record.value2 = float(record.value) / 100
    