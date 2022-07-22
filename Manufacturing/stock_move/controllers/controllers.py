# -*- coding: utf-8 -*-
# from odoo import http


# class StockMove(http.Controller):
#     @http.route('/stock_move/stock_move', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_move/stock_move/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_move.listing', {
#             'root': '/stock_move/stock_move',
#             'objects': http.request.env['stock_move.stock_move'].search([]),
#         })

#     @http.route('/stock_move/stock_move/objects/<model("stock_move.stock_move"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_move.object', {
#             'object': obj
#         })
