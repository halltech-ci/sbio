# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomProduct(http.Controller):
#     @http.route('/hta_custom_product/hta_custom_product', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_product/hta_custom_product/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_product.listing', {
#             'root': '/hta_custom_product/hta_custom_product',
#             'objects': http.request.env['hta_custom_product.hta_custom_product'].search([]),
#         })

#     @http.route('/hta_custom_product/hta_custom_product/objects/<model("hta_custom_product.hta_custom_product"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_product.object', {
#             'object': obj
#         })
