from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosPaymentCommands(models.TransientModel):
    _name = "barcode.printer.wizard"
    _description = "Barcode Printer Number"


    number = fields.Integer()
    

    def printer_barcode(self):
      
        data = {
                    'model':'barcode.printer.wizard',
                    'form': self.read()[0],

                    }
        return self.env.ref('barcode_product.pos_report_assign_order').with_context(landscape=True).report_action(self, data=data)

        


