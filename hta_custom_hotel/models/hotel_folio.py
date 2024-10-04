# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

FOLIO_STATE = [("draft", "Draft"),
              ("sent", "Envoyé"),
              ("sale", "Confirmé"),
              ("done", "Checkout"),
              ("cancel", "Annulé")]

class HotelFolio(models.Model):
    _inherit = "hotel.folio"

    reservation_ids = fields.Many2many("hotel.reservation", string="Rservations")
    checkout_date = fields.Datetime(tracking=True, readonly=False)
    room_line_ids = fields.One2many("hotel.folio.line")
    service_line_ids = fields.One2many("hotel.service.line")
    #state = fields.Selection(FOLIO_STATE ,tracking=True)
    product_ids = fields.Many2many("product.product", compute="_compute_room_ids", store=True)

    @api.depends("room_line_ids.product_id")
    def _compute_room_ids(self):
        for rec in self:
            #product_ids = rec.room_line_ids.filtered(lambda l:l.product_id.isroom)
            product_ids = rec.room_line_ids.mapped("product_id")
            rec.product_ids = product_ids

    def action_done(self):
        res = super(HotelFolio, self).action_done()
        if self.reservation_id:
            date_now = fields.Datetime.now()
            reservation = self.reservation_id
            reservation.write({
                "state": "close",
                "checkout" : date_now,
            })
            reservation._onchange_check_dates()
        return res

    '''def action_done(self):
        res = super(HotelFolio, self).action_done()
        for line in self.room_line_ids:
            date_now = fields.Datetime.now()
            room = line.product_id
            if line.checkout_date.date() <= date_now.date():
                romm.write({
                    "status": "available"
                })
            else:
                line.write({
                    "checkout_date": date_now,
                })
                romm.write({
                    "status": "available"
                })
        return res

    def update_checkout(self):
        for line in self.room_line_ids:
            date_now = fields.Datetime.now()
            room = line.product_id
            if line.checkout_date.date() <= date_now.date():
                romm.write({
                    "status": "available"
                })
            else:
                line.write({
                    "checkout_date": date_now,
                })
                romm.write({
                    "status": "available"
                })
        return res
    '''    
                
        

    