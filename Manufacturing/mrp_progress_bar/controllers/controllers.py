# -*- coding: utf-8 -*-
# from odoo import http


# class MrpProgressBar(http.Controller):
#     @http.route('/mrp_progress_bar/mrp_progress_bar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_progress_bar/mrp_progress_bar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_progress_bar.listing', {
#             'root': '/mrp_progress_bar/mrp_progress_bar',
#             'objects': http.request.env['mrp_progress_bar.mrp_progress_bar'].search([]),
#         })

#     @http.route('/mrp_progress_bar/mrp_progress_bar/objects/<model("mrp_progress_bar.mrp_progress_bar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_progress_bar.object', {
#             'object': obj
#         })
