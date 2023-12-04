from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosAssignCommands(models.TransientModel):
    _name = "pos.audit.commands.wizard"
    _description = "Audit Validate"


    date_audit = fields.Datetime(string='Date Audit', required=True, default=fields.Datetime.now())
    commande = fields.Text(string='Commande')
    
#     state = fields.Selection(selection_add=[('')])
    
    @api.onchange('date_audit')
    def _onchange_partner(self):
        texte = ""
        for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            texte += order.name + " ;"
        self.commande = texte
        
    def validate_audit_orders(self):
        for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            order_lines = order.lines
            order.write({'audit':'valide', 'date_audit': self.date_audit})
            


