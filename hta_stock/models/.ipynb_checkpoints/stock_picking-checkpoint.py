# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    receipt_user = fields.Many2one('res.users', string="Utlisateur Receip")
    
    def button_my_custom_action(self):
        if self.receipt_user:
            if self.receipt_user != self.env.user:
                raise AccessError(_("Vous n'êtes pas autorisé à effectuer cette action."))
        return self.button_validate()
