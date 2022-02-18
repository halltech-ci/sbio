# -*- coding: utf-8 -*-
# from odoo import http


# class HtaPos(http.Controller):
#     @http.route('/hta_pos/hta_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_pos/hta_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_pos.listing', {
#             'root': '/hta_pos/hta_pos',
#             'objects': http.request.env['hta_pos.hta_pos'].search([]),
#         })

#     @http.route('/hta_pos/hta_pos/objects/<model("hta_pos.hta_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_pos.object', {
#             'object': obj
#         })
