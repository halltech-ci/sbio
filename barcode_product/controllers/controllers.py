# -*- coding: utf-8 -*-
# from odoo import http


# class BarcodeProduct(http.Controller):
#     @http.route('/barcode_product/barcode_product', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barcode_product/barcode_product/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('barcode_product.listing', {
#             'root': '/barcode_product/barcode_product',
#             'objects': http.request.env['barcode_product.barcode_product'].search([]),
#         })

#     @http.route('/barcode_product/barcode_product/objects/<model("barcode_product.barcode_product"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barcode_product.object', {
#             'object': obj
#         })
