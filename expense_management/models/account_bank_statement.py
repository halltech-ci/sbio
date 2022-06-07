# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    expense_ids = fields.One2many('expense.request', 'statement_id')
    
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    
    
    '''def get_credit_account(self):
        res = self.env['account.account'].search([]).filtered(lambda l:l.date.month==month and l.journal_id.type in ('cash'))
        return res
    '''
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags', 
        #domain="['|', ('company_id', '=', company_id), ('company_id', '=', False)]", 
        relation='account_statement_model_analytic_tag_rel'
    )
    debit = fields.Monetary(currency_field='journal_currency_id')
    #credit_account = fields.Monetary(currency_field='journal_currency_id')
    expense_id = fields.Many2one('expense.request',"Expense")
    project_id = fields.Many2one("project.project", "Project",store=True)
    credit_account = fields.Many2one('account.account', string='Credit Account')
    debit_account = fields.Many2one('account.account',string='Debit Account')
    p_amount = fields.Float("Montant", digits='Product Price', compute='_compute_p_amount')
    
    @api.depends('amount')
    def _compute_p_amount(self):
        for line in self:
            line.p_amount = -line.amount
    """        
    def _prepare_expense_move(self, move_ref):
        ref = move_ref or ''
        if self.ref
    """
   
    
    #Method for reconcile expense line
    """def create_move_values(self):
        #res = super(ExpenseRequest, self).create_move_values()
        for line in self:
            move_value = {
                'ref': self.name,
                'date': self.date,
                'journal_id': self.statement_id.journal_id.id,
                'company_id': company.id,
            }
            date = self.date
            name = self.name
            analytic_account = self.analytic_account_id.id
            analytic_tags = self.analytic_tag_ids.ids
            partner = self.partner_id.id
            amount = self.amount
            account = self.account_id.id#La contrepartie
            journal = self.journal_id
            
        for request in self:
            ref = request.name
            account_date = fields.Date.today()#self.date
            journal = request.journal
            company = request.company_id
            analytic_account = request.analytic_account
            move_value = {
                'ref':ref,
                'date': account_date,
                'journal_id': journal.id,
                'company_id': company.id,
            }
            expense_line_ids = []
            lines = request.mapped('line_ids')
            for line in lines:
                if not (line.employee_id.address_home_id.property_account_payable_id):
                    raise UserError(_('Pas de compte pour : "%s" !') % (line.employee_id))
                partner_id = line.employee_id.address_home_id.id
                debit_line = (0, 0, {
                    'name': line.name,
                    'account_id': line.debit_account,
                    'debit': line.amount > 0.0 and line.amount or 0.0,
                    'credit': line.amount < 0.0 and -line.amount or 0.0, 
                    'partner_id': partner_id,
                    'journal_id': journal.id,
                    'date': account_date,
                    'analytic_account_id': analytic_account.id,

                })
                expense_line_ids.append(debit_line)
                credit_line = (0, 0, {
                    'name': line.name,
                    'account_id': line.employee_id.address_home_id.property_account_payable_id.id,
                    'debit': line.amount < 0.0 and line.amount or 0.0,
                    'credit': line.amount > 0.0 and -line.amount or 0.0, 
                    'partner_id': partner_id,
                    'journal_id': journal.id,
                    'date': account_date,
                    'analytic_account_id': analytic_account.id,

                })
                expense_line_ids.append(credit_line)
            move_value['line_ids'] = expense_line_ids
            move = self.env['account.move'].create(move_value)
            request.write({'move_id': move.id})
            move.post()"""
    


    
