# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    def check(self):
        res = super(PosMakePayment, self).check()
        
        order = self.env['pos.order'].browse(self.env.context.get('active_id', False))
        order.write({
            "payment_date": self.payment_date.date()
        })
        '''lines = order.lines
        if order.state == "draft":
            livraison = lines.filtered(lambda l: "ivraison" in l.full_product_name)
            if livraison:
                livraison.write({
                    "price_unit": 0,
                    "price_subtotal": 0,
                    "price_subtotal_incl": 0
                })
                livraison._onchange_amount_line()
            order._onchange_amount_all()
        '''    