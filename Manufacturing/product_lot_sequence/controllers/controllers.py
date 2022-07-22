# -*- coding: utf-8 -*-
# from odoo import http


# class ProductLotSequence(http.Controller):
#     @http.route('/product_lot_sequence/product_lot_sequence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_lot_sequence/product_lot_sequence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_lot_sequence.listing', {
#             'root': '/product_lot_sequence/product_lot_sequence',
#             'objects': http.request.env['product_lot_sequence.product_lot_sequence'].search([]),
#         })

#     @http.route('/product_lot_sequence/product_lot_sequence/objects/<model("product_lot_sequence.product_lot_sequence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_lot_sequence.object', {
#             'object': obj
#         })
