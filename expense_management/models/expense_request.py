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
READONLY_STATES = {
        'to_cancel': [('readonly', True)],
        }


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
    total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_amount', store=True, tracking=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account', check_company=True,)
    #project_id = fields.Many2one('project.project', string='Projet')
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    journal = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['cash', 'bank'])], states=STATES, default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))
    statement_id = fields.Many2one('account.bank.statement', string="Caisse", tracking=True, states=READONLY_STATES,)
    statement_line_ids = fields.One2many('account.bank.statement.line', 'expense_id')
    move_ids = fields.Many2many('account.move', string='Account Move')
    is_expense_approver = fields.Boolean(string="Is Approver", compute="_compute_is_expense_approver",)
    expense_approver = fields.Many2one('res.users', string="Valideur", states=READONLY_STATES)
    balance_amount = fields.Monetary('Solde Caisse', currency_field='currency_id', related='statement_id.balance_end')
    
    
    @api.depends('line_ids.amount')
    def _compute_amount(self):
        for request in self:
            request.total_amount = sum(request.line_ids.mapped('amount'))
    
    @api.depends("state")
    def _compute_to_approve_allowed(self):
        for rec in self:
            rec.to_approve_allowed = rec.state == "validate"
            
    """This method will check approver limit"""
    @api.depends('total_amount', 'company_id.approve_limit_1', 'company_id.approve_limit_2')
    def _compute_is_expense_approver(self):
        for req in self:
            limit_1 = req.company_id.approve_limit_1
            limit_2 = req.company_id.approve_limit_2
            user = self.env.user
            if user.has_group('expense_management.group_expense_approver_3'):
                req.is_expense_approver = True
            elif user.has_group('expense_management.group_expense_approver_2'):
                if req.total_amount <= limit_2:
                    req.is_expense_approver = True
                else:
                    req.is_expense_approver = False
            elif user.has_group('expense_management.group_expense_approver_1'):
                if req.total_amount <= limit_1:
                    req.is_expense_approver = True
                else:
                    req.is_expense_approver = False
            else:
                req.is_expense_approver = False
    
    def button_to_cancel(self):        
        return self.write({'state': 'to_cancel'})#Annuler
    
    def button_authorize(self):
        if self.state not in  ['approve']:
            raise UserError(
                    _(
                        "Vous ne pouvez pas autoriser un dépense non approuvée!"
                    )
                )
        for line in self.line_ids:
            line.action_authorize()
        return self.write({'state': 'authorize'})
    
    def button_to_approve(self):
        self.to_approve_allowed_check()
        for line in self.line_ids:
            line.action_to_approve()
        return self.write({"state": "to_approve"})
    
    def button_approve(self):
        self.is_approver_check()
        self.write({'statement_id' : self.get_default_statement_id()})
        if not self.statement_id:
            raise UserError(
                    _(
                        "Veuillez contacter la comptabilite pour creer le journal caisse."
                    )
                )
        if self.total_amount > self.balance_amount:
            raise UserError(
                    _(
                        "Solde caisse insuffisant. Veillez faire un appro"
                    )
                )
        for line in self.line_ids:
            line.action_approve()
        return self.write({"state": "approve"})
    
    def to_validate(self):
        for line in self.line_ids:
            line.action_validate()
        return self.write({'state': 'validate'})
    
    def button_rejected(self):
        self.is_approver_check()
        if any(self.filtered(lambda expense: expense.state in ('post'))):
            raise UserError(_('You cannot reject expense which is approve or paid!'))
        self.mapped("line_ids").do_cancel()
        return self.write({"state": "draft"})
    
    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "Vous ne pouvez pas faire cette action. Veuillez demander approbation pour"
                        ". (%s)"
                    )
                    % rec.name
                )
    def is_approver_check(self):
        for rec in self:
            if not rec.is_expense_approver:
                raise UserError(
                    _(
                        "Vous ne pouvez pas approuver cette demande. Problème de droit! "
                        ". (%s)"
                    )
                    % rec.name
                )
    
    def is_approve_check(self):
        for rec in self:
            if rec.balance_amount < rec.total_amount:
                raise UserError(
                    _(
                        "Solde en caisse insuffisant pour payer cette note de frais "
                        ". (%s)"
                    )
                    % rec.balance_amount
                )
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('expense.request.code') or '/'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('expense.request.code') or '/'
        request = super(ExpenseRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ExpenseRequest, self).write(vals)
        return res
    
    def unlink(self):
        if any(self.filtered(lambda expense: expense.state not in ('draft'))):
            raise UserError(_('Vous ne pouvez pas supprimer une note de frais !'))        
        return super(ExpenseRequest, self).unlink()