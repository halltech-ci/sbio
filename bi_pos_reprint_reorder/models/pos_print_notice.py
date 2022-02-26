from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime

class pos_order_notice(models.Model):
    _inherit = 'pos.order'
    
    def print_notice_product(self):
        orderlines = []
        for orderline in self.lines:
            new_vals = {
				'product_id': orderline.product_id.name,
                'notice':orderline.product_id.notice_fields,
                }
            orderlines.append(new_vals)
        vals = {
			'orderlines': orderlines,
			'barcode': self.barcode,
			'user_name' : self.user_id.name,
            # Partner
            'partner_name':self.partner_id.name,
            'partner_phone':self.partner_id.phone,
		}
        return vals
    
#     def print_notice_product(self):
        
#         orderlines = []
# 		for orderline in self.lines:
# 			new_vals = {
# 				'product_id': orderline.product_id.name,
#                 'notice':orderline.product_id.notice_fields,
# 				}
# 			orderlines.append(new_vals)
#         vals = {
# 			'orderlines': orderlines,
# 			'barcode': self.barcode,
# 			'user_name' : self.user_id.name,
#             # Partner
#             'partner_name':self.partner_id.name,
#             'partner_phone':self.partner_id.phone,
# 		}
#         return vals
