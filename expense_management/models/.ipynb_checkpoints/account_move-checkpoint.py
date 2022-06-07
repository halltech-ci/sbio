# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move.line"
    
    expense_line_id = fields.Many2one('expense.line', string='Expense Line')