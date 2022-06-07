# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    expense_ids = fields.One2many('expense.request', 'statement_id')
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags', relation='account_statement_model_analytic_tag_rel')
    debit = fields.Monetary(currency_field='currency_id')
    expense_id = fields.Many2one('expense.request',"Expense")
    project_id = fields.Many2one("project.project", "Project",store=True)
    credit_account = fields.Many2one('account.account', string='Credit Account')
    debit_account = fields.Many2one('account.account',string='Debit Account')
    p_amount = fields.Float("Montant", digits='Product Price', compute='_compute_p_amount')
    
    @api.depends('amount')
    def _compute_p_amount(self):
        for line in self:
            line.p_amount = -line.amount
    