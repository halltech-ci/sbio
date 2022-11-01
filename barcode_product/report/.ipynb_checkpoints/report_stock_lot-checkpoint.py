from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportBarcodeReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.barcode_product.report_stock_lot_barcode_wizard_number'
    
    _description = 'Barcode wizard '
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        number = data['form']['number']
        
        docs = []
        stock_lot = data['form']['stock_lot'][0]
        lines = self.env['stock.production.lot'].search([('id','=',stock_lot)])
       
        docs.append ({
                    'lines': lines,
                })
             
        return {
            'doc_model': 'barcode.printer.wizard',
            'numbers': number,
            'docs': docs,
            'lines':lines
        }
    

    