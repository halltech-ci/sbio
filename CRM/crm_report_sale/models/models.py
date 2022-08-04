# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class crm_report_sale(models.Model):
#     _name = 'crm_report_sale.crm_report_sale'
#     _description = 'crm_report_sale.crm_report_sale'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
