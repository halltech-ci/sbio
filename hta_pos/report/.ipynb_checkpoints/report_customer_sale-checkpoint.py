from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.report_pos_custmer_sale_'
    
    _description = 'Rapport liste des client/Articles'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        amount_min = data['form']['amount_min']
        amount = data['form']['amount']
        docs = []
        
        pos_list = self.env['pos.order'].search([])
        
        res_partner = self.env['res.partner'].search([])
        for res_p in res_partner:
            id_partner = res_p.id
            partner_name = res_p.name
            partner_phone = res_p.phone
            montant = 0
            pos_list = self.env['pos.order'].search([('partner_id','=',id_partner),('date_order','>=',date_start),('date_order','<=',date_end)])
            for line in pos_list:
                montant = montant + line.amount_paid
            
            if (amount_min > 0 and amount_min <= montant and amount > montant):
            
                docs.append ({
                            'type':"Montant compris entre ",
                            'partner_name': partner_name,
                            'partner_phone':partner_phone,
                            'montant':montant,
                    })
            elif(montant >= amount):
                docs.append ({
                            'type': "Montant Superieur à",
                            'partner_name': partner_name,
                            'partner_phone':partner_phone,
                            'montant':montant,
                    })
                
             
        return {
            'doc_model': 'report.pos.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }

class ReportPosReporttXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.customer_sale_report_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Cash XLM'
    
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('RAPPORT DES CLIENTS SUR UNE PERIODE')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 28,
                    'font_color': 'black', 'bold': True, 'border': 1})
        
        montant_initial = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 16,
                    'font_color': 'black','bold': True,})
        
        table_header = workbook.add_format(
                {'bg_color': 'black', 'align': 'center', 'font_size': 18,
                    'font_color': 'white'})
        table_body_space = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
        table_body_line = workbook.add_format(
                {'bg_color': '#eee8e2', 'align': 'center', 'font_size': 15,
                    'font_color': 'black', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        table_recap = workbook.add_format(
                {'bg_color': '#f05987', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_recap_solde = workbook.add_format(
                {'bg_color': '#98ec6e', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        
        
        
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        amount_min = data.get('amount_min')
        amount = data.get('amount')
        docs = []
        res_partner = self.env['res.partner'].search([])
        for res_p in res_partner:
            id_partner = res_p.id
            partner_name = res_p.name
            partner_phone = res_p.phone
            montant = 0
            pos_list = self.env['pos.order'].search([('partner_id','=',id_partner),('date_order','>=',date_start),('date_order','<=',date_end)])
            for line in pos_list:
                montant = montant + line.amount_paid
            
            if (amount_min > 0 and amount_min <= montant and montant < amount):
            
                docs.append ({
                            'type':"Montant compris entre ",
                            'partner_name': partner_name,
                            'partner_phone':partner_phone,
                            'montant':montant,
                    })
            elif(montant >= amount):
                docs.append ({
                            'type': "Montant Superieur à",
                            'partner_name': partner_name,
                            'partner_phone':partner_phone,
                            'montant':montant,
                    })
            
        sheet.set_column('A:A', 40)
        
        row = 2
        col = 0
        
        sheet.merge_range(row, col, row+1, col+5, 'RAPPORT POINT DE VENTE', title)
            
        row += 5
        col = 0
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 30)
        
        
        
        sheet.merge_range(row, col, row+1, col, 'Client', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Téléphone', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Montant', table_header)
        # Header row
        
        
        
        ligne = 10
        i = 0
        for line in docs:
            sheet.write(ligne+i, col, line['partner_name'])
            sheet.write(ligne+i, col+1, line['partner_phone'])
            sheet.write(ligne+i, col+2, line['montant'])
            i +=1
