# -*- coding: utf-8 -*-
# from odoo import http


# class HtaInheritPos(http.Controller):
#     @http.route('/hta_inherit_pos/hta_inherit_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_inherit_pos/hta_inherit_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_inherit_pos.listing', {
#             'root': '/hta_inherit_pos/hta_inherit_pos',
#             'objects': http.request.env['hta_inherit_pos.hta_inherit_pos'].search([]),
#         })

#     @http.route('/hta_inherit_pos/hta_inherit_pos/objects/<model("hta_inherit_pos.hta_inherit_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_inherit_pos.object', {
#             'object': obj
#         })
