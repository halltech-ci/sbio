# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
import datetime
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError
class HtaPartner(models.Model):
    _inherit = 'res.partner'

    total_amount_pos = fields.Float(store=True,compute='_compute_total_pos', string="Montant Total")
    phone = fields.Char(unique=True)
    
    @api.constrains('phone')
    def _check_phone_unique(self):
        for partner in self:
            if partner.phone and self.search_count([('id', '!=', partner.id), ('phone', '=', partner.phone)]) > 0:
                raise exceptions.ValidationError('Ce numéro de téléphone existe déjà pour un autre client.')

    @api.depends('pos_order_ids')
    def _compute_total_pos(self):
        for record in self:
            if record.pos_order_ids:
                for rs in record.pos_order_ids:
                    record.total_amount_pos = record.total_amount_pos + rs.amount_paid
    
    
    
    
    def merge_duplicate_partners(self):
        # Trouver les clients dupliqués avec le même numéro de téléphone
        partners = self.env['res.partner'].search([])
        duplicates = {}
        for partner in partners:
            if partner.phone:
                if partner.phone not in duplicates:
                    duplicates[partner.phone] = [partner]
                else:
                    duplicates[partner.phone].append(partner)

        # Fusionner les clients et transférer les ventes
        for phone, partners in duplicates.items():
            if len(partners) > 1:
                partner_to_keep = partners[0]
                partners_to_merge = partners[1:]
                for partner in partners_to_merge:
                    pos_orders = partner.pos_order_ids.filtered(lambda x: x.state != 'cancel')
                    for pos_order in pos_orders:
                        pos_order.partner_id = partner_to_keep
                    pos_orders = partner.sale_order_ids.filtered(lambda x: x.state != 'cancel')
                    for pos_order in pos_orders:
                        pos_order.partner_id = partner_to_keep
                    partner.write({'active': False})
                    self.env.cr.commit()


        # Afficher un message de confirmation
        # message = "Les clients dupliqués ont été fusionnés avec succès."
        # self.env.user.notify_warning(message, title='Fusion de clients')

        return True