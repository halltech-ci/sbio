# -*- coding: utf-8 -*-
# from odoo import http


# class ButtonReports(http.Controller):
#     @http.route('/button_reports/button_reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/button_reports/button_reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('button_reports.listing', {
#             'root': '/button_reports/button_reports',
#             'objects': http.request.env['button_reports.button_reports'].search([]),
#         })

#     @http.route('/button_reports/button_reports/objects/<model("button_reports.button_reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('button_reports.object', {
#             'object': obj
#         })
