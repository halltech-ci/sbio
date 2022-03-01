# -*- coding: utf-8 -*-
# from odoo import http


# class HtaResPartner(http.Controller):
#     @http.route('/hta_res_partner/hta_res_partner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_res_partner/hta_res_partner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_res_partner.listing', {
#             'root': '/hta_res_partner/hta_res_partner',
#             'objects': http.request.env['hta_res_partner.hta_res_partner'].search([]),
#         })

#     @http.route('/hta_res_partner/hta_res_partner/objects/<model("hta_res_partner.hta_res_partner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_res_partner.object', {
#             'object': obj
#         })
