# -*- coding: utf-8 -*-
# from odoo import http


# class RapportNotice(http.Controller):
#     @http.route('/rapport_notice/rapport_notice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rapport_notice/rapport_notice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rapport_notice.listing', {
#             'root': '/rapport_notice/rapport_notice',
#             'objects': http.request.env['rapport_notice.rapport_notice'].search([]),
#         })

#     @http.route('/rapport_notice/rapport_notice/objects/<model("rapport_notice.rapport_notice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rapport_notice.object', {
#             'object': obj
#         })
