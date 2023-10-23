# -*- coding: utf-8 -*-
# from odoo import http


# class PosDeliveryOrder(http.Controller):
#     @http.route('/pos_delivery_order/pos_delivery_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_delivery_order/pos_delivery_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_delivery_order.listing', {
#             'root': '/pos_delivery_order/pos_delivery_order',
#             'objects': http.request.env['pos_delivery_order.pos_delivery_order'].search([]),
#         })

#     @http.route('/pos_delivery_order/pos_delivery_order/objects/<model("pos_delivery_order.pos_delivery_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_delivery_order.object', {
#             'object': obj
#         })
