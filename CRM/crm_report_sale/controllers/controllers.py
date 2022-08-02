# -*- coding: utf-8 -*-
# from odoo import http


# class CrmReportSale(http.Controller):
#     @http.route('/crm_report_sale/crm_report_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_report_sale/crm_report_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_report_sale.listing', {
#             'root': '/crm_report_sale/crm_report_sale',
#             'objects': http.request.env['crm_report_sale.crm_report_sale'].search([]),
#         })

#     @http.route('/crm_report_sale/crm_report_sale/objects/<model("crm_report_sale.crm_report_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_report_sale.object', {
#             'object': obj
#         })
