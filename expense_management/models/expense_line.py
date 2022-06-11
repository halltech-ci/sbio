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

class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    
    name = fields.Char(string='Description')
    request_id = fields.Many2one('expense.request')
