# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    expense_id = fields.Many2one('expense.request')

class AccountMove(models.Model):
    _inherit = "account.move.line"
    
    expense_line_id = fields.Many2one('expense.line', string='Expense Line')