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
    
    def get_lines(self, product_id, date_start,date_end):
        
        #params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT rpo.product_id AS product, SUM(rpo.price_sub_total) AS price_sub_total, SUM(rpo.product_qty) AS product_qty, rp.name AS customer_name, rp.phone AS customer_phone
                FROM report_pos_order AS rpo
                INNER JOIN product_product AS pp ON  pp.id = rpo.product_id
                INNER JOIN res_partner AS rp ON rp.id = rpo.partner_id

                WHERE 
                   (rpo.product_id = """+ product_id+""")
                    AND
                    (x_aml.date BETWEEN '%s' AND '%s')
                GROUP BY product
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        
        docs = []
        if data['form']['product_id']:
            product_id = data['form']['product_id'][0]
            lines = self.env['product.product'].search([('id','=',product_id)])
        else:
            lines = self.env['product.product'].search([])
        for line in lines:
            prod_id = line.id
            id_pp = str(prod_id)
            
            get_lines = self.get_lines(id_pp,date_start,date_end)
            #name = line.name
            
            docs.append ({
                #'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'report.pos.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }
    
    