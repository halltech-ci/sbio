# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime

READONLY_STATES = {
        'to_cancel': [('readonly', True)],
        }

class ExpenseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Custom expense request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code("expense.request.code")
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)

    def get_default_statement_id(self):
        date = datetime.date.today()
        month = date.month
        res = self.env['account.bank.statement'].search([]).filtered(lambda l:l.date.month==month and l.journal_id.type in ('cash'))
        if not res:
            raise UserError(
                    _(
                        "Veuillez contacter la comptabilite pour creer le journal caisse."
                    )
                )
        return res
    
    name = fields.Char(default='/',)
    description = fields.Char('Description', required=True)
    state = fields.Selection(selection=[
        ('draft', 'Broullon'),
        ('submit', 'Soumis'),
        ('validate', 'Validate'),
        ('to_approve', 'A approuver'),
        ('approve', 'Approuve'),
        ('authorize','Autorise'),
        ('to_cancel', 'Annule'),
        ('post', 'Paye'),
        ('reconcile', 'Lettre'),
        ('cancel', 'Rejete')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    """employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id, check_company=True)"""
    
    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line', states={'to_cancel': [('readonly', True)]})
    intermediary = fields.Many2one('hr.employee', string="Intermediaire")
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    date = fields.Datetime(default=fields.Datetime.now, string="Date",
                          #readonly=True, 
                          )
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_amount', store=True, tracking=True)
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
    
    def send_validation_mail(self):
        self.ensure_one()
        template_id = self.env.ref('expense_management.expense_mail_template').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        
    @api.onchange('state')
    def _onchange_state(self):
        if self.state in ['authorize']:
            if self.statement_id != self.get_default_cash_journal():
                self.statement_id = self.get_default_cash_journal()
    
    
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
                
    @api.onchange('company_id')
    def _onchange_expense_company_id(self):
        self.employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid), ('company_id', '=', self.company_id.id)])
    
    @api.depends('line_ids.amount')
    def _compute_amount(self):
        for request in self:
            request.total_amount = sum(request.line_ids.mapped('amount'))
    
      
    def button_reconcile_expense(self):
        #self.ensure_one()
        action = self.env.ref('expense_management.act_bank_stline_reconcile')
        result = action.read()[0]
              
    def action_reconcile_expense(self):
        self.ensure_one()
        lines = self.line_ids
        return {
            'type':'ir.actions.client',
            'tag': 'expense_line_reconcile_action',
            'target': 'new',
            'context': {'expense_line_ids': self.line_ids, 'company_ids': self.mapped('company_id').ids} ,           
        }
    
    def get_expense_line(self):
        #lines = self.env['expense.request'].mapped('self.line_ids')
        return self.mapped('line_ids')   

    
    """This create account_bank_statetment_line in bank_statement given in expense request"""
    def create_bank_statement(self):
        self.ensure_one()
        for request in self:
            ref = request.description
            statement_id = request.statement_id
            journal_id = request.journal.id
            company = request.company_id.id
            expense_lines = request.mapped('line_ids')
            value = []
            for line in expense_lines:
                #ref = line.name
                name = line.name
                partner_id = line.employee_id.address_home_id.id
                if line.amount < 0:
                    amount = line.amount
                else:
                    amount = -line.amount
                #amount = line.amount
                project_id = line.project.id
                lines = (0, 0, {
                    "name": line.name,
                    #"partner_id": line.employee_id.address_home_id.id,
                    'amount': amount,
                    'project_id': line.project.id,
                    'analytic_account_id': line.analytic_account.id,
                    'expense_id': line.request_id.id,
                    'credit_account': line.request_id.journal.default_credit_account_id.id,
                })
                value.append(lines)
            statement_id.write({'line_ids': value})
        return True
    
    def action_post(self):
        date = datetime.date.today()
        month = date.month
        if self.state == 'post':
            raise UserError(
                    _(
                        "Vous ne pouvez pas payer une note déja payée"
                    )
                )
        res = self.env['account.bank.statement'].search([]).filtered(lambda l:l.date.month==month and l.journal_id.type in ('cash'))
        if res.id != self.statement_id.id:
            self.write({'statement_id': self.get_default_statement_id()})
        post = self.create_bank_statement()
        if post:
            #st_lines = self.env['account.bank.statement.line'].search([('expense_id', '=', rec.id)]).ids
            for line in self.line_ids:
                line.action_post()
            return self.write({'state': 'post',})
        return True
    
    def _create_analytic_line(self):
        '''Create analytic lines from statement_line_ids in each expense_request'''
        for request in self:
            account = request.analytic_account
            lines = self.mapped('statement_line_ids')
            res = []
            for line in lines:
                aal = (0, 0, {
                    'name': line.name,
                    'ref': line.name,
                    'unit_amount': 1,
                    'amount': -line.amount,
                    #'account_id': line.analytic_account.id,
                    'expense_line': line.id,
                    'company_id': request.company_id.id,
                    'move_id': line.move_id.id,
                })
                res.append(aal)
            account.write({'line_ids' : res})
                
    
    def create_move_values(self):
        self.ensure_one()
        for request in self:
            #expense_line = request.statement_line_ids
            account_src = request.journal.default_credit_account_id.id
            ref = request.statement_id.name
            journal = request.journal
            company = request.company_id
            account_date = fields.Date.today()
            move_value = {
                    'ref': ref,
                    'date': account_date,
                    'journal_id': journal.id,
                    'company_id': company.id,
                }
            move = self.env['account.move'].create(move_value)
            lines = self.mapped('statement_line_ids')
            move_lines = []
            for line in lines:
                partner = line.partner_id
                debit_account = line.debit_account
                line.write({'move_id': move.id})
                debit_line = (0, 0, {
                    'name': line.name,
                    'account_id': debit_account.id,
                    'debit': line.p_amount > 0.0 and line.p_amount or 0.0,
                    'credit': line.p_amount < 0.0 and -line.p_amount or 0.0, 
                    'partner_id': partner.id,
                    'journal_id': journal.id,
                    'date': account_date,
                    'statement_id': self.statement_id.id,
                    'statement_line_id': line.id,
                    'analytic_account_id': line.analytic_account_id.id and line.analytic_account_id or line.project_id.analytic_account_id.id,
                })
                move_lines.append(debit_line)
                credit_line = (0, 0, {
                    'name': line.name,
                    'account_id': account_src,
                    'debit': line.p_amount < 0.0 and -line.p_amount or 0.0,
                    'credit': line.p_amount > 0.0 and line.p_amount or 0.0, 
                    'partner_id': partner.id,
                    'journal_id': journal.id,
                    'date': account_date,
                    #'analytic_account_id': line.analytic_account_id.id or line.project_id.analytic_account_id.id,
                    #'reconciled': True,
                    'statement_id': self.statement_id.id,
                    'statement_line_id': line.id,
                })
                move_lines.append(credit_line)
                #move_value['line_ids'] = move_lines
                move = self.env['account.move'].write({'line_ids': move_lines})
                move.write({'expense_id': request.id})
            move.post()
            request.write({'state': 'reconcile'})
            #request._create_analytic_line()
        return True
    
    def action_submit(self):
        for line in self.line_ids:
            line.action_submit()
        self.state = "submit"
        return True
    
    def button_to_cancel(self):
        #self.is_approver_check()
        #self.mapped("line_ids").do_cancel()
        
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
        #self.is_approver_check()
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
    