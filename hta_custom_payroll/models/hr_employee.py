# -*- coding: utf-8 -*-

from odoo import models, fields, api


# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit="hr.employee"
    
    hiring_date = fields.Date(string='Hiring Start Date', related="contract_id.date_start")
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    seniority = fields.Integer(string="Anciennete", store=True, compute='_compute_seniority')
    nbre_part = fields.Float(string="Nombre de Part", default=1)
    qualification = fields.Char(string='Qualification')
    categorie = fields.Char(string='Categorie')
    rib = fields.Char(string="RIB")
    #Traitement special AVS, pret
    pret_employe = fields.Monetary(string='Pret employe', company_dependent=True, currency_field='currency_id')
    avs = fields.Monetary(string='Avance sur salaire', company_dependent=True, currency_field='currency_id')
    # Account 
    account_debit = fields.Many2one('account.account', 'Debit Account', company_dependent=True, domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Credit Account', company_dependent=True, domain=[('deprecated', '=', False)])

    
    @api.depends('hiring_date')
    def _compute_seniority(self):
        today = fields.Date.today()
        today_date = fields.Date.from_string(today)
        for rec in self:
            if rec.hiring_date:
                age = today_date - fields.Date.from_string(rec.hiring_date)
                rec.seniority = int(age.days/366)
            else:
                rec.seniority = 0
                
    def _get_overtime(self, date_from, date_to):
        pass
    

    
    