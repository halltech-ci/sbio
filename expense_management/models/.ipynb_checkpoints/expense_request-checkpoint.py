# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ExpenseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Custom expense request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    @api.model
    def _get_default_requested_by(self):
        return self.env['res.users'].browse(self.env.uid)
    
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code("expense.request.code")


    def get_default_cash_journal(self):


        import datetime
        date = datetime.date.today()
        month = date.month
        res = self.env['account.bank.statement'].search([]).filtered(lambda l:l.date.month==month)
        return res
    
    name = fields.Char( default=_get_default_name)

    description = fields.Char('Description', required=True)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('validate', 'Validate'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('authorize','Autoriser'),
        ('to_cancel', 'Annuler'),
        ('post', 'Paid'),
        #('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    """employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_employee_id, check_company=True)"""
    
    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line')
    intermediary = fields.Many2one('hr.employee', string="Intermediaire")
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange',
                    default=_get_default_requested_by)
    date = fields.Datetime(readonly=True, default=fields.Datetime.now, string="Date")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    total_amount = fields.Monetary('Total Amount', currency_field='currency_id', compute='_compute_amount', store=True, tracking=True)
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    project_id = fields.Many2one('project.project', string='Projet')
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    journal = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['cash', 'bank'])], default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))

    statement_id = fields.Many2one('account.bank.statement', string="Caisse", tracking=True,default=lambda self: self.get_default_cash_journal())

    move_id = fields.Many2one('account.move', string='Account Move')
    is_expense_approver = fields.Boolean(string="Is Approver",
        compute="_compute_is_expense_approver",
    )
    expense_approver = fields.Many2one('res.users', string="Valideur")
    balance_amount = fields.Monetary('Solde Caisse', currency_field='currency_id', related='statement_id.balance_end')
    
    
#     @api.model
#     def create(self, vals):
#         if vals.get('name', _('New')) == _('New'):
#             vals['name'] = self.env['ir.sequence'].next_by_code('expense.request.code') or _('Error')
#         result = super(ExpenseRequest, self).create(vals)
#         return result
    
    
    def send_validation_mail(self):
        self.ensure_one()
        template_id = self.env.ref('expense_management.expense_mail_template').id
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        
    
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
            
    """This create account_bank_statetment_line in bank_statement given in expense request"""
    def create_bank_statement(self):
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
                    "partner_id": line.employee_id.address_home_id.id,
                    'amount': amount,
                    'project_id': line.project.id,
                    'analytic_account_id': line.analytic_account.id,

                    'expense_id': line.request_id.id,

                })
                value.append(lines)
            statement_id.write({'line_ids': value})
        return True
            
    def action_post(self):
        if self.state == 'post':
            raise UserError(
                    _(
                        "You can not post request already in posted state"
                    )
                )
        post = self.create_bank_statement()
        if post:
            for line in self.line_ids:
                line.action_post()
            return self.write({'state': 'post'})
        return True
    
    def action_submit(self):
        for line in self.line_ids:
            line.action_submit()
        self.state = "submit"
        return True
    
    def button_to_cancel(self):
        #self.is_approver_check()
        #self.mapped("line_ids").do_cancel()
        
        return self.write({'state': 'to_cancel'})
    
    def button_authorize(self):

        #self.is_approver_check()

        #self.is_approve_check()
        for line in self.line_ids:
            line.action_approve()
        return self.write({'state': 'authorize'})
    
    def button_to_approve(self):
        self.to_approve_allowed_check()
        #self.is_approver_check()
        for line in self.line_ids:
            line.action_to_approve()
        return self.write({"state": "to_approve"})
    
    def button_approve(self):
        self.is_approver_check()
        #self.is_approve_check()
        for line in self.line_ids:
            line.action_approve()
        return self.write({"state": "approve"})
    
    def to_validate(self):
        for line in self.line_ids:
            line.action_validate()
        return self.write({'state': 'validate'})
    
    def button_rejected(self):
        self.is_approver_check()
        if any(self.filtered(lambda expense: expense.state in ('approve', 'post'))):
            raise UserError(_('You cannot reject expense which is approve or paid!'))
        self.mapped("line_ids").do_cancel()
        return self.write({"state": "draft"})
    
    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a expense request "
                        "which is not submited. (%s)"
                    )
                    % rec.name
                )
    def is_approver_check(self):
        for rec in self:
            if not rec.is_expense_approver:
                raise UserError(
                    _(
                        "You are not allowed to approve this expense request "
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
        request = super(ExpenseRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ExpenseRequest, self).write(vals)
        return res
    
    def unlink(self):
        if any(self.filtered(lambda expense: expense.state not in ('draft', 'cancel', 'submitted'))):
            raise UserError(_('You cannot delete a expense which is not draft, cancelled or submitted!'))
        for expense in self:
            if not expense.state == 'to_cancel':
                raise UserError(_('In order to delete a expense request, you must cancel it first.'))
                
        return super(ExpenseRequest, self).unlink()
    