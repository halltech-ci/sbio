# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomHotel(http.Controller):
#     @http.route('/hta_custom_hotel/hta_custom_hotel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_hotel/hta_custom_hotel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_hotel.listing', {
#             'root': '/hta_custom_hotel/hta_custom_hotel',
#             'objects': http.request.env['hta_custom_hotel.hta_custom_hotel'].search([]),
#         })

#     @http.route('/hta_custom_hotel/hta_custom_hotel/objects/<model("hta_custom_hotel.hta_custom_hotel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_hotel.object', {
#             'object': obj
#         })
