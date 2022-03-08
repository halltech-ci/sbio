# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleSsbio(http.Controller):
#     @http.route('/hta_sale_ssbio/hta_sale_ssbio', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_ssbio/hta_sale_ssbio/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_ssbio.listing', {
#             'root': '/hta_sale_ssbio/hta_sale_ssbio',
#             'objects': http.request.env['hta_sale_ssbio.hta_sale_ssbio'].search([]),
#         })

#     @http.route('/hta_sale_ssbio/hta_sale_ssbio/objects/<model("hta_sale_ssbio.hta_sale_ssbio"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_ssbio.object', {
#             'object': obj
#         })
