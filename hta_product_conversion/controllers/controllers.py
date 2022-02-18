# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductConversion(http.Controller):
#     @http.route('/hta_product_conversion/hta_product_conversion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_conversion/hta_product_conversion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_conversion.listing', {
#             'root': '/hta_product_conversion/hta_product_conversion',
#             'objects': http.request.env['hta_product_conversion.hta_product_conversion'].search([]),
#         })

#     @http.route('/hta_product_conversion/hta_product_conversion/objects/<model("hta_product_conversion.hta_product_conversion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_conversion.object', {
#             'object': obj
#         })
