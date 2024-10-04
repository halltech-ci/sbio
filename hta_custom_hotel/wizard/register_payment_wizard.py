# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


class RegistrationPaymentWizard(models.TransientModel):
    _name = "reservation.register.payment.wizard"
    _description = "hotel reservation register payment wizard"
    
    
    amount = fields.Float(string="Montant")
    partner_id = fields.Many2one("res.partner")
    date = fields.Date(default=fields.Date.today())
    journal = fields.Many2one('account.journal', domain=['|', ('type', '=', 'cash'), ('type', '=', 'bank')])
    reservation_id = fields.Many2one('hotel.reservation')
    ref = fields.Char(string="Note", help="Enregistrer la référence du payement")
    journal_type = fields.Selection(related="journal.type")
    reservation_casher = fields.Many2one('res.users', string="Réceptionnniste")
    company_id = fields.Many2one("res.company", default=lambda self:self.env.company)
    
    def action_create_payment(self):
        if self.amount <= 0:
            raise ValidationError(_("Veuillez saisir un montant positif"))
        payment_methods = self.journal.inbound_payment_method_line_ids
        if payment_methods :
            payment_methods = payment_methods[0].id
        payment_vals = {
            'payment_type' : "inbound",
            'partner_type':'customer',
            'amount' : self.amount,
            #'communication' : self.name,
            'ref': self.ref,
            'date' : self.date,
            'journal_id' : self.journal.id,
            'payment_method_line_id': payment_methods or False,
            'partner_id': self.partner_id.id,
            'currency_id': self.company_id.currency_id.id,
            'reservation_id': self.reservation_id.id,
            'user_id': self.reservation_casher.id,
        }
        payment =  self.env['account.payment'].sudo().create(payment_vals)
        payment.action_post()
        credit_aml = payment.line_ids.filtered('credit')
        self.reservation_id.write(
                {"amount_paid": self.reservation_id.amount_paid + self.amount, 
                 "memo": self.ref,
                 "reservation_casher":self.reservation_casher.id
                }
            )
    
    