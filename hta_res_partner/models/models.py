# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hta_res_partner(models.Model):
#     _name = 'hta_res_partner.hta_res_partner'
#     _description = 'hta_res_partner.hta_res_partner'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
