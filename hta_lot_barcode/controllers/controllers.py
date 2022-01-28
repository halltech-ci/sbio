# -*- coding: utf-8 -*-
# from odoo import http


# class HtaLotBarcode(http.Controller):
#     @http.route('/hta_lot_barcode/hta_lot_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_lot_barcode/hta_lot_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_lot_barcode.listing', {
#             'root': '/hta_lot_barcode/hta_lot_barcode',
#             'objects': http.request.env['hta_lot_barcode.hta_lot_barcode'].search([]),
#         })

#     @http.route('/hta_lot_barcode/hta_lot_barcode/objects/<model("hta_lot_barcode.hta_lot_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_lot_barcode.object', {
#             'object': obj
#         })
