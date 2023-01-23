# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCoupon(http.Controller):
#     @http.route('/hta_coupon/hta_coupon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_coupon/hta_coupon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_coupon.listing', {
#             'root': '/hta_coupon/hta_coupon',
#             'objects': http.request.env['hta_coupon.hta_coupon'].search([]),
#         })

#     @http.route('/hta_coupon/hta_coupon/objects/<model("hta_coupon.hta_coupon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_coupon.object', {
#             'object': obj
#         })
