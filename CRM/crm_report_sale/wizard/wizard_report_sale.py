# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class SaleNumberLotReportWizard(models.TransientModel):
    _name = 'report.number.lot.wizard'
    _description = "Rapport PDV"
    

    date_start = fields.Date(string='Debut', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Fin', required=True, default=fields.Date.today)
    number_lot = fields.Many2many('stock.production.lot', string="Numero de lot")

    def get_report(self):
        data = {
            'model':'report.pos.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('crm_report_sale.report_pos_lot_sale_pdf').with_context(landscape=True).report_action(self, data=data)

    
    # def get_generate_xlsx_report(self):
    #     data = {
    #         'date_start': self.date_start,
    #         'date_end': self.date_end,
    #         'number_lot': self.number_lot.ids,
    #     }
    #     # ref `module_name.report_id` as reference.
    #     return self.env.ref('crm_report_sale.pos_report_generate_xlsx_report').report_action(self, data=data)
