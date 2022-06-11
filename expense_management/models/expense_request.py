# -*- coding: utf-8 -*-

from odoo import models, fields, api

STATES = [('draft', 'Broullon'),
        ('submit', 'Soumis'),
        ('validate', 'Validate'),
        ('to_approve', 'A approuver'),
        ('approve', 'Approuve'),
        ('authorize','Autorise'),
        ('to_cancel', 'Annule'),
        ('post', 'Paye'),
        ('reconcile', 'Lettre'),
        ('cancel', 'Rejete')
    ]    


class ExpenseRequest(models.Model):
    _name = "expense.request"
    _description = "Manage expense request workflow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(default='/',)
    description = fields.Char('Description', required=True)
    state = fields.Selection(selection=STATES, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    