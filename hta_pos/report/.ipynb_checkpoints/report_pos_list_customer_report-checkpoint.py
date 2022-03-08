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
    
    def get_lines(self, product_id,date_start,date_end):
        
        params = [date_start,date_end]
        query = """
                SELECT rp.name AS customer_name, rp.phone AS customer_phone, SUM(rpo.price_sub_total) AS price_sub_total, SUM(rpo.product_qty) AS product_qty
                FROM report_pos_order AS rpo
                INNER JOIN res_partner AS rp ON rp.id = rpo.partner_id
                INNER JOIN product_product AS prod ON prod.id = rpo.product_id
                WHERE 
                   (prod.id = """+product_id+""")
                    AND
                    (rpo.date BETWEEN %s AND %s)
                GROUP BY customer_name,customer_phone
        """

        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        docs = []
        if data['form']['product_id']:
            product_id = data['form']['product_id'][0]
<<<<<<< HEAD
            lines = self.env['product.product'].search([('product_id','=',product_id)])
=======
            lines = self.env['product.product'].search([('id','=',product_id)])
>>>>>>> main_dev
        else:
            lines = self.env['product.product'].search([])
        for line in lines:
            prod_id = line.id
            id_pp = str(prod_id)
            name = line.partner_ref
            get_lines = self.get_lines(id_pp,date_start,date_end)
            
            
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
    
    