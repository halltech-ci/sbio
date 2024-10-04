# -*- coding: utf-8 -*-

from odoo import models, fields, api


STATE = [
    ("draft", "Draft"),
    ("confirm", "Check In"),
    ("cancel", "Cancel"),
    ("done", "Checked In"),
    ("close", "Checked Out"),
]

RESERVATION_STATE = [
    ("in_progess", "En cours"),
    ("expired", "En cours")
]

class HotelReservation(models.Model):
    _inherit = "hotel.reservation"

    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    amount_paid = fields.Monetary(currency_field='currency_id', store=True, string="Acompte", tracking=True)
    reservation_casher = fields.Many2one("res.users")
    memo = fields.Char()
    room_ids = fields.Many2many("hotel.room", compute="compute_room_ids", store=True)
    state = fields.Selection(selection_add=STATE, readonly=True, default="draft", tracking=True)
    checkout = fields.Datetime("Expected-Date-Departure", required=True, tracking=True, readonly=False)
    folio_state = fields.Selection(related="folio_id.state")
    date_order = fields.Datetime(readonly=False,)
    
    def update_reservation_state(self):
        for rec in self:
            if rec.folio_id:
                if rec.folio_id.state == "done":
                    rec.state = "close"

    @api.depends("reservation_line.reserve")
    def compute_room_ids(self):
        for rec in self:
            rec.room_ids = rec.reservation_line.reserve

    def register_payment(self):
        view = self.env.ref('hta_custom_hotel.reservation_regster_payment_wizard')
        return{
            'name':"Enregister payment",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'reservation.register.payment.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            #'domain': [('id', 'in', active_ids), ('delivery_id', '!=', True)],
            'context': {
                'default_partner_id': self.partner_id.id, 
                'default_reservation_id':self.id,
                "default_reservation_casher":self.env.uid,
            },
        }