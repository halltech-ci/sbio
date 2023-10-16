# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"

    payment_status = fields.Selection(selection=[("paid", "Payé"), ("none", "Non payé"), ("partial", "Partiel"), ("gift", "Gratuit")], string="Status payement", compute="_compute_payment_status",)
    amount_due = fields.Float(compute="_compute_amount_due", string="Créance")
    amount_discount = fields.Float(string="Remise", compute="_compute_amount_discount")

    @api.depends("lines.discount")
    def _compute_amount_discount(self):
        for rec in self:
            rec.amount_discount = sum([line.discount for line in rec.lines])
            
    @api.depends("amount_paid", "amount_total", "amount_discount")
    def _compute_payment_status(self):
        for rec in self:
            rec.payment_status = "none"
            if rec.amount_paid == rec.amount_total:
                rec.payment_status = "paid"
            if rec.amount_paid > 0 and rec.amount_paid < rec.amount_total:
                rec.payment_status = "partial"
            if all([int(line.discount) == 100 for line in rec.lines]):
                rec.payment_status = "gift"
                

    @api.depends("amount_paid", "amount_total")
    def _compute_amount_due(self):
        for rec in self:
            rec.amount_due = rec.amount_total - rec.amount_paid
        