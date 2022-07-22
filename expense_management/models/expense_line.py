# -*- coding: utf-8 -*-

from odoo import models, fields, api


REQUEST_STATE = [('draft', 'Broullon'),
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

class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    @api.model
    def _get_employee_id_domain(self):
        employee_ids = self.env['hr.employee'].search([]).ids
        res = [('address_home_id.property_account_payable_id', '!=', False), ('id', 'in', employee_ids)]
        
        return res
    
    name = fields.Char(string='Description')
    request_id = fields.Many2one('expense.request')
    expense_type = fields.Boolean(string="Imputer au projet", default=True)
    request_id = fields.Many2one('expense.request', string='Expense Request')
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', index=True, readonly=True, copy=False, default='draft', required=True, help='Expense Report State')
    date = fields.Datetime(readonly=True, related='request_id.date', string="Date")
    amount = fields.Float("Montant", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one('res.partner', string="Fournisseur", )
    requested_by = fields.Many2one('res.users' ,'Demandeur', related='request_id.requested_by')
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account/Projet')
    analytic_line = fields.Many2one('account.analytic.line', string="Analytic_line")
    expense_type = fields.Boolean(string="Imputer au projet", default=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    accounting_date = fields.Date(string='Accounting Date')
    debit_account = fields.Many2one('account.account', string='Debit Account')
    credit_account = fields.Many2one('account.account', string='Credit Account')
    transfer_amount = fields.Float('Frais de transfert', digits='Product Price')
    employee_id = fields.Many2one('hr.employee', string="Beneficiaire", required=True, check_company=True, domain=lambda self: self._get_employee_id_domain())
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
    
