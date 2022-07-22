# -*- coding: utf-8 -*-
# from odoo import http


# class MrpProduction(http.Controller):
#     @http.route('/mrp_production/mrp_production', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_production/mrp_production/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_production.listing', {
#             'root': '/mrp_production/mrp_production',
#             'objects': http.request.env['mrp_production.mrp_production'].search([]),
#         })

#     @http.route('/mrp_production/mrp_production/objects/<model("mrp_production.mrp_production"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_production.object', {
#             'object': obj
#         })
