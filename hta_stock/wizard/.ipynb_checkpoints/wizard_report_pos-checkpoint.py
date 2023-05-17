# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _name = 'report.pos.wizard'
    _description = "Rapport PDV"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    product_id = fields.Many2many('product.product', string="Article")
    
    filter_pdv = fields.Selection([('RIVIERA', 'RIVIERA'),('LATRILLE', 'LATRILLE'),('PRIMA', 'PRIMA')], string='Filtre Par PDV',default='RIVIERA',)

    def get_report(self):
        data = {
            'model':'report.pos.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_stock.pos_report_list_product_sale').with_context(landscape=True).report_action(self, data=data)

    