# -*- coding: utf-8 -*-
# from odoo import http


# class HtaGenerateBarcode(http.Controller):
#     @http.route('/hta_generate_barcode/hta_generate_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_generate_barcode/hta_generate_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_generate_barcode.listing', {
#             'root': '/hta_generate_barcode/hta_generate_barcode',
#             'objects': http.request.env['hta_generate_barcode.hta_generate_barcode'].search([]),
#         })

#     @http.route('/hta_generate_barcode/hta_generate_barcode/objects/<model("hta_generate_barcode.hta_generate_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_generate_barcode.object', {
#             'object': obj
#         })
