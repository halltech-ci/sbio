# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

PAYMENT_MODE = [('justify', 'Employee (To justify)'),
                ('company', 'Company (Not justify)'),
                ('reimburse', 'Employee (To Reimburse)'),
               ]

PAYMENT_TYPE = [('cash', 'Espece'),
                ('trasfert', 'Mobile'),
                ('check', 'Cheque'),
               ]

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('validate', 'Validate'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('authorize','Autoriser'),
        ('to_cancel', 'Annuler'),
        ('post', 'Paid'),
        #('done', 'Paid'),
        ('cancel', 'Refused')
        ]


class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    #_order = 'date desc'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    @api.model
    def _get_employee_id_domain(self):
        employee_ids = self.env['hr.employee'].search([]).ids
        res = [('address_home_id.property_account_payable_id', '!=', False), ('id', 'in', employee_ids)]
        
        return res

    @api.model
    def _get_analytic_domain(self):
        project_ids = self.env['project.project'].search([]).ids
        res = [('project_ids', 'not in', project_ids)]
        return res
    
    @api.model
    def _get_project_domain(self):
        project_ids = self.env['project.project'].search([]).ids
        res = [('id', 'in', project_ids)]
        return res
    
    name = fields.Char('Description', required=True)
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Beneficiaire", required=True, check_company=True, domain=lambda self: self._get_employee_id_domain())
    expense_type = fields.Boolean(string="Imputer au projet", default=True)
    request_id = fields.Many2one('expense.request', string='Expense Request')
    date = fields.Datetime(readonly=True, related='request_id.date', string="Date")
    amount = fields.Float("Montant", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, 
                                 default=lambda self: self.env.company
                                )
    partner_id = fields.Many2one('res.partner', string="Fournisseur", 
                                 #domain=lambda self: self._get_employee_id_domain()
                                )
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange', related='request_id.requested_by')
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account/Projet', domain=lambda self: self._get_analytic_domain())
    analytic_line = fields.Many2one('account.analytic.line', string="Analytic_line")
    expense_type = fields.Boolean(string="Imputer au projet", default=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, 
                                  default=lambda self: self.env.company.currency_id
                                 )
    accounting_date = fields.Date(string='Accounting Date')
    debit_account = fields.Many2one('account.account', string='Debit Account')
    credit_account = fields.Many2one('account.account', string='Credit Account')
    transfer_amount = fields.Float('Frais de transfert', digits='Product Price')
    project = fields.Many2one('project.project', string='Project', domain=lambda self: self._get_project_domain())
    expense_product = fields.Many2one('product.product', string='Product', domain="[('can_be_expensed', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", ondelete='restrict')
    move_id = fields.Many2one('account.move', string="Account Move")
    
    
    def action_submit(self):
        self._action_submit()

    def _action_submit(self):
        self.request_state = "submit"
        
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "approve"  
    
    def to_approve(self):
        self.request_state = "validate"
    
    def action_authorize(self):
        self.request_state = "authorize"
    
    def action_post(self):
        self.request_state = "post"
    
    def action_validate(self):
        self.request_state = "validate"
        
    def do_cancel(self):
        """Actions to perform when cancelling a expense line."""
        self.write({"request_state": 'draft'})
    
    def unlink(self):
        for expense in self:
            if expense.request_state in ['post',]:
                raise UserError(_('Vous ne pouvez pas supprimer une dépense déja payée'))
        return super(ExpenseLine, self).unlink()

    def write(self, vals):
        return super(ExpenseLine, self).write(vals)
    
