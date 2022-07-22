# -*- coding: utf-8 -*-
# from odoo import http


# class MrpProductConversion(http.Controller):
#     @http.route('/mrp_product_conversion/mrp_product_conversion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_product_conversion/mrp_product_conversion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_product_conversion.listing', {
#             'root': '/mrp_product_conversion/mrp_product_conversion',
#             'objects': http.request.env['mrp_product_conversion.mrp_product_conversion'].search([]),
#         })

#     @http.route('/mrp_product_conversion/mrp_product_conversion/objects/<model("mrp_product_conversion.mrp_product_conversion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_product_conversion.object', {
#             'object': obj
#         })
