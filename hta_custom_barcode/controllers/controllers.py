# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomBarcode(http.Controller):
#     @http.route('/hta_custom_barcode/hta_custom_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_barcode/hta_custom_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_barcode.listing', {
#             'root': '/hta_custom_barcode/hta_custom_barcode',
#             'objects': http.request.env['hta_custom_barcode.hta_custom_barcode'].search([]),
#         })

#     @http.route('/hta_custom_barcode/hta_custom_barcode/objects/<model("hta_custom_barcode.hta_custom_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_barcode.object', {
#             'object': obj
#         })
