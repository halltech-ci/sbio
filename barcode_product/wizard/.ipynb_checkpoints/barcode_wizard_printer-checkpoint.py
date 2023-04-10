from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosPaymentCommands(models.TransientModel):
    _name = "barcode.printer.wizard"
    _description = "Barcode Printer Number"


    number = fields.Integer()
    stock_lot = fields.Many2one('stock.production.lot', required=True)
    

    def printer_barcode(self):
      
        data = {
                    'model':'barcode.printer.wizard',
                    'form': self.read()[0],
                    }
        return self.env.ref('barcode_product.barcode_printer_number').with_context(landscape=True).report_action(self, data=data)

        


