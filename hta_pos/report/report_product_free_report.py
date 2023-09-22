from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT



class ReportPosReporttXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.product_free_generate_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Produit gratuit'
    

    
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('RAPPORT DES PRODUIT GRATUIT')
        
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
        
   
            
        sheet.set_column('A:A', 40)
        
        row = 2
        col = 0
        
        sheet.merge_range(row, col, row+1, col+5, 'RAPPORT DES PRODUIT GRATUIT', title)
            
        row += 5
        col = 0
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 30)
        
        
        
        sheet.merge_range(row, col, row+1, col, 'Client', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Téléphone', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Date Commande', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Produit', table_header)
        sheet.merge_range(row, col+4, row+1, col+4, 'Qté', table_header)
        sheet.merge_range(row, col+5, row+1, col+5, 'Commercial(e)', table_header)
        # Header row
        
        
        
        ligne = 10
        i = 0
        for line in data.get('listproduit'):
            sheet.write(ligne+i, col, line.get('partner'))
            sheet.write(ligne+i, col+1, line.get('phone'))
            sheet.write(ligne+i, col+2, line.get('date'))
            sheet.write(ligne+i, col+3, line.get('name'))
            sheet.write(ligne+i, col+4, line.get('quantite'))
            sheet.write(ligne+i, col+5, line.get('commercial'))
            i +=1
