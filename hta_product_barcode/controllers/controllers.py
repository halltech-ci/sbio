# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductBarcode(http.Controller):
#     @http.route('/hta_product_barcode/hta_product_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_barcode/hta_product_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_barcode.listing', {
#             'root': '/hta_product_barcode/hta_product_barcode',
#             'objects': http.request.env['hta_product_barcode.hta_product_barcode'].search([]),
#         })

#     @http.route('/hta_product_barcode/hta_product_barcode/objects/<model("hta_product_barcode.hta_product_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_barcode.object', {
#             'object': obj
#         })
