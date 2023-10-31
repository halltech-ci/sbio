# -*- coding: utf-8 -*-
# from odoo import http


# class HtaStock(http.Controller):
#     @http.route('/hta_stock/hta_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_stock/hta_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_stock.listing', {
#             'root': '/hta_stock/hta_stock',
#             'objects': http.request.env['hta_stock.hta_stock'].search([]),
#         })

#     @http.route('/hta_stock/hta_stock/objects/<model("hta_stock.hta_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_stock.object', {
#             'object': obj
#         })
