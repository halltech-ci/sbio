# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class ReportCustomerSale(models.TransientModel):
    _name = 'report.sale.customer.report.wizard'
    _description = "Rapport Client"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    filter_by = fields.Selection([('entre_deux', 'Entre deux montant'), ('un_montant', 'Superieur à un montant')], string='Filter', default='Filter')
    amount_min = fields.Float(string='Montant Minimum')
    amount = fields.Float(string='Montant Superieur')

    def get_report(self):
        data = {
            'model':'report.sale.customer.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_pos.pos_report_customer_list_product').with_context(landscape=True).report_action(self, data=data)

    
    def get_generate_xlsx_report(self):
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'filter_by': self.filter_by,
            'amount_min': self.amount_min,
            'amount': self.amount,
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_pos.pos_report_generate_xlsx_report').report_action(self, data=data)