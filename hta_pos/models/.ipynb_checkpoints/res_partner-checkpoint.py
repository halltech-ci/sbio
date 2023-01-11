# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
class HtaPartner(models.Model):
    _inherit = 'res.partner'

    total_amount_pos = fields.Float(store=True,compute='_compute_total_pos', string="Montant Total")

    @api.depends('pos_order_ids')
    def _compute_total_pos(self):
        for record in self:
            if record.pos_order_ids:
                for rs in record.pos_order_ids:
                    record.total_amount_pos = record.total_amount_pos + rs.amount_paid
            