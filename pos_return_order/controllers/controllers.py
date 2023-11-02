# -*- coding: utf-8 -*-
# from odoo import http


# class PosReturnOrder(http.Controller):
#     @http.route('/pos_return_order/pos_return_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_return_order/pos_return_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_return_order.listing', {
#             'root': '/pos_return_order/pos_return_order',
#             'objects': http.request.env['pos_return_order.pos_return_order'].search([]),
#         })

#     @http.route('/pos_return_order/pos_return_order/objects/<model("pos_return_order.pos_return_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_return_order.object', {
#             'object': obj
#         })
