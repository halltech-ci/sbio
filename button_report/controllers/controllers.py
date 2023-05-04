# -*- coding: utf-8 -*-
# from odoo import http


# class ButtonReport(http.Controller):
#     @http.route('/button_report/button_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/button_report/button_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('button_report.listing', {
#             'root': '/button_report/button_report',
#             'objects': http.request.env['button_report.button_report'].search([]),
#         })

#     @http.route('/button_report/button_report/objects/<model("button_report.button_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('button_report.object', {
#             'object': obj
#         })
