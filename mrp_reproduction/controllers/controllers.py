# -*- coding: utf-8 -*-
# from odoo import http


# class MrpReproduction(http.Controller):
#     @http.route('/mrp_reproduction/mrp_reproduction', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_reproduction/mrp_reproduction/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_reproduction.listing', {
#             'root': '/mrp_reproduction/mrp_reproduction',
#             'objects': http.request.env['mrp_reproduction.mrp_reproduction'].search([]),
#         })

#     @http.route('/mrp_reproduction/mrp_reproduction/objects/<model("mrp_reproduction.mrp_reproduction"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_reproduction.object', {
#             'object': obj
#         })
