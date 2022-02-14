from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosAssignCommands(models.TransientModel):
    _name = "pos.assign.commands.wizard"
    _description = "Assign Commands Pos"

    delivery_person = fields.Many2one(
        comodel_name="res.partner",
        string="Delivery Person",
        required=True,
        domain=[("person_delivery", "=", True)],
    )
    date_delivery = fields.Date(string='Date Livraison', required=True, default=fields.Date.today)
    
    
    def assign_delivery_orders(self):
        for record in self._context.get('active_ids'):
            pos_order = self.env[self._context.get('active_model')].browse(record)
            if pos_order.delivery_person:
                raise UserError(_("LES COMMANDES SONT DEJA ASSIGNER"))
            else:
                pos_order.delivery_person = self.delivery_person
                pos_order.date_delivery = self.date_delivery


