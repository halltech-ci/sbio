# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    expense_ids = fields.One2many('expense.request', 'statement_id')
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null')
    debit = fields.Monetary()
    expense_id = fields.Many2one('expense.request',"Expense")
    #project_id = fields.Many2one("project.project", "Project",store=True)
    credit_account = fields.Many2one('account.account', string='Credit Account')
    debit_account = fields.Many2one('account.account',string='Debit Account')
    move_id = fields.Many2one('account.move')
    
    def create_account_move_id(self, move):
        for line in self:
            line.write({'move_id': move})