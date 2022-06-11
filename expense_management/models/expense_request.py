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
    _check_company = True
    
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    name = fields.Char(default='/',)
    description = fields.Char('Description', required=True)
    state = fields.Selection(selection=STATES, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line', states={'to_cancel': [('readonly', True)]})
    intermediary = fields.Many2one('hr.employee', string="Intermediaire")
    requested_by = fields.Many2one('res.users' ,'Demandeur', tracking=True, default=_get_default_requested_by)
    date = fields.Datetime(default=fields.Datetime.now, string="Date", readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    """total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_amount', store=True, tracking=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account', check_company=True,)
    project_id = fields.Many2one('project.project', string='Projet')
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    journal = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['cash', 'bank'])], states=READONLY_STATES, default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))

    statement_id = fields.Many2one('account.bank.statement', string="Caisse", tracking=True, states=READONLY_STATES,)
    statement_line_ids = fields.One2many('account.bank.statement.line', 'expense_id')
    move_ids = fields.Many2many('account.move', string='Account Move')
    is_expense_approver = fields.Boolean(string="Is Approver",
        compute="_compute_is_expense_approver",
    )
    expense_approver = fields.Many2one('res.users', string="Valideur", states=READONLY_STATES)
    balance_amount = fields.Monetary('Solde Caisse', currency_field='currency_id', related='statement_id.balance_end')
    """