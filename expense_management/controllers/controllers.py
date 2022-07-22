# -*- coding: utf-8 -*-
# from odoo import http


# class ExpenseManagement(http.Controller):
#     @http.route('/expense_management/expense_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expense_management/expense_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('expense_management.listing', {
#             'root': '/expense_management/expense_management',
#             'objects': http.request.env['expense_management.expense_management'].search([]),
#         })

#     @http.route('/expense_management/expense_management/objects/<model("expense_management.expense_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expense_management.object', {
#             'object': obj
#         })
