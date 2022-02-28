from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportTimeSheetReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_pos.report_pos_delivery_order'
    
    _description = 'Rapport liste des client/Articles'
    
#     def get_lines(self, product_id,date_start,date_end):
        
#         params = [date_start,date_end]
#         query = """
#                 SELECT rp.name AS customer_name, rp.phone AS customer_phone, SUM(rpo.price_sub_total) AS price_sub_total, SUM(rpo.product_qty) AS product_qty
#                 FROM report_pos_order AS rpo
#                 INNER JOIN res_partner AS rp ON rp.id = rpo.partner_id
#                 INNER JOIN product_product AS prod ON prod.id = rpo.product_id
#                 WHERE 
#                    (prod.id = """+product_id+""")
#                     AND
#                     (rpo.date BETWEEN %s AND %s)
#                 GROUP BY customer_name,customer_phone
#         """

#         self.env.cr.execute(query,params)
#         return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_delivery = data['form']['date_delivery']
        delivery_person = data['form']['delivery_person']
        
        orders = data['orders']
        
             
        return {
            'doc_model': 'pos.assign.commands.wizard',
            'date_delivery': date_delivery,
            'delivery_person': delivery_person,
            'orders': orders,
            
        }
    
    