# -*- coding: utf-8 -*-
# from odoo import http


# class MrpProductionRequest(http.Controller):
#     @http.route('/mrp_production_request/mrp_production_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_production_request/mrp_production_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_production_request.listing', {
#             'root': '/mrp_production_request/mrp_production_request',
#             'objects': http.request.env['mrp_production_request.mrp_production_request'].search([]),
#         })

#     @http.route('/mrp_production_request/mrp_production_request/objects/<model("mrp_production_request.mrp_production_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_production_request.object', {
#             'object': obj
#         })
