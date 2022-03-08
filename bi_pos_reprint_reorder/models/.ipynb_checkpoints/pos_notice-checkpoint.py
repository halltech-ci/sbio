# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime


class pos_order_notice(models.Model):
	_inherit = 'pos.order'
    
#     def notice_print(self):
#         orderlines = []
#         paymentlines = []
#         for orderline in self.lines:
#             new_vals = {
#                 'product_id': orderline.full_product_name,
#                 'notice':orderline.notice,
#                 }
#             orderlines.append(new_vals)
#         vals = {
#             'orderlines': orderlines,
#             'barcode': self.barcode,
#             'user_name' : self.user_id.name,

#             'partner_name':self.partner_id.name,
#             'partner_phone':self.partner_id.phone,
#         }

#         return vals