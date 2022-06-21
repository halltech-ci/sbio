# -*- coding: utf-8 -*-
# from odoo import http


# class ReportAccount(http.Controller):
#     @http.route('/report_account/report_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_account/report_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_account.listing', {
#             'root': '/report_account/report_account',
#             'objects': http.request.env['report_account.report_account'].search([]),
#         })

#     @http.route('/report_account/report_account/objects/<model("report_account.report_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_account.object', {
#             'object': obj
#         })
