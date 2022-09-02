from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.report_pos_custmer_product'
    
    _description = 'Rapport liste des client/Articles'
    
    def get_lines(self, entrepot,product_id,date_start,date_end):

            params = [date_start,date_end]
            query = """
                    SELECT rp.name AS customer_name, rp.phone AS customer_phone,rpo.date AS date_order, SUM(rpo.price_sub_total) AS price_sub_total, SUM(rpo.product_qty) AS product_qty, sw.name AS entrepot
                    FROM report_pos_order AS rpo
                    INNER JOIN res_partner AS rp ON rp.id = rpo.partner_id
                    INNER JOIN product_product AS prod ON prod.id = rpo.product_id
                    INNER JOIN pos_config AS pos_conf ON pos_conf.id = rpo.config_id
                    INNER JOIN stock_warehouse AS sw ON sw.id = pos_conf.warehouse_id
                    WHERE
                        (sw.id = """+entrepot+""")
                        AND
                       (prod.id = """+product_id+""")
                        AND
                        (rpo.date BETWEEN %s AND %s)
                    GROUP BY customer_name,customer_phone,date_order,entrepot
            """

            self.env.cr.execute(query,params)
            return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        docs = []
        if data['form']['locations']:
            locations = data['form']['locations']
            stok_locs = self.env['stock.warehouse'].search([('id','in',locations)])
        else:
            stok_locs = self.env['stock.warehouse'].search([])
            
        if data['form']['product_id']:
            product_id = data['form']['product_id']
            lines = self.env['product.product'].search([('id','in',product_id)])
        else:
            lines = self.env['product.product'].search([])
        for wh in stok_locs:
            entrep = wh.id
            id_entre = str(entrep)
            for line in lines:
                prod_id = line.id
                id_pp = str(prod_id)
                name = line.partner_ref
                get_lines = self.get_lines(id_entre,id_pp,date_start,date_end)
            
            
                docs.append ({
                        'id_pp': id_pp,
                        'name':name,
                        'get_lines':get_lines,
                })
             
        return {
            'doc_model': 'report.pos.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            
            'get_lines':self.get_lines,
        }
    

    

class ReportPosReporttXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.pos_report_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Cash XLM'
    

    
    def get_lines(self, entrepot,product_id,date_start,date_end):

            params = [date_start,date_end]
            query = """
                    SELECT rp.name AS customer_name, rp.phone AS customer_phone,rpo.date AS date_order, SUM(rpo.price_sub_total) AS price_sub_total, SUM(rpo.product_qty) AS product_qty, sw.name AS entrepot
                    FROM report_pos_order AS rpo
                    INNER JOIN res_partner AS rp ON rp.id = rpo.partner_id
                    INNER JOIN product_product AS prod ON prod.id = rpo.product_id
                    INNER JOIN pos_config AS pos_conf ON pos_conf.id = rpo.config_id
                    INNER JOIN stock_warehouse AS sw ON sw.id = pos_conf.warehouse_id
                    WHERE
                        (sw.id = """+entrepot+""")
                        AND
                       (prod.id = """+product_id+""")
                        AND
                        (rpo.date BETWEEN %s AND %s)
                    GROUP BY customer_name,customer_phone,date_order,entrepot
            """

            self.env.cr.execute(query,params)
            return self.env.cr.dictfetchall()
    
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('RAPPORT POINT DE VENTE')
        
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
        
        docs = []
        if data.get('locations'):
            locations = data.get('locations')
            stok_locs = self.env['stock.warehouse'].search([('id','in',locations)])
        else:
            stok_locs = self.env['stock.warehouse'].search([])
        if data.get('product_id'):
            product_id = data.get('product_id')
            lines = self.env['product.product'].search([('id','in',product_id)])
        else:
            lines = self.env['product.product'].search([])
        
        for wh in stok_locs:
            entrep = wh.id
            id_entre = str(entrep)
            for line in lines:
                prod_id = line.id
                id_pp = str(prod_id)
                name = line.partner_ref
                get_lines = self.get_lines(id_entre,id_pp,date_start,date_end)
            
            
                docs.append ({
                    'id_pp': id_pp,
                    'name':name,
                    'get_lines':get_lines,
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
        sheet.merge_range(row, col+2, row+1, col+2, 'Date Commande', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Produit', table_header)
        sheet.merge_range(row, col+4, row+1, col+4, 'Qté', table_header)
        sheet.merge_range(row, col+5, row+1, col+5, 'Entrepôt', table_header)
        # Header row
        
        
        
        ligne = 10
        i = 0
        for line in docs:
            for cash in line['get_lines']:
                sheet.write(ligne+i, col, cash.get('customer_name'))
                sheet.write(ligne+i, col+1, cash.get('customer_phone'))
                sheet.write(ligne+i, col+2, cash.get('date_order').strftime('%d/%m/%Y'))
                sheet.write(ligne+i, col+3, line['name'])
                sheet.write(ligne+i, col+4, cash.get('product_qty'))
                sheet.write(ligne+i, col+5, cash.get('entrepot'))
                i +=1
