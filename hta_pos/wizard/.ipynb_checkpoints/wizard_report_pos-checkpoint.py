# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _name = 'report.pos.report.wizard'
    _description = "Rapport PDV"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    product_id = fields.Many2one('product.product', string="Article")

    def get_report(self):
        data = {
            'model':'report.pos.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
<<<<<<< HEAD
        return self.env.ref('hta_pos.pos_report_customer_list_product').with_context(landscape=True).report_action(self, data=data)
=======
        return self.env.ref('hta_pos.account_analytic_report').with_context(landscape=True).report_action(self, data=data)
>>>>>>> main_dev

