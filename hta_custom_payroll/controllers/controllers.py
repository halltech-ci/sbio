# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomPayroll(http.Controller):
#     @http.route('/hta_custom_payroll/hta_custom_payroll', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_payroll/hta_custom_payroll/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_payroll.listing', {
#             'root': '/hta_custom_payroll/hta_custom_payroll',
#             'objects': http.request.env['hta_custom_payroll.hta_custom_payroll'].search([]),
#         })

#     @http.route('/hta_custom_payroll/hta_custom_payroll/objects/<model("hta_custom_payroll.hta_custom_payroll"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_payroll.object', {
#             'object': obj
#         })
