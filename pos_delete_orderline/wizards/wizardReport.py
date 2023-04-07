from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class CreateWizardReport(models.TransientModel):
    _name = "create.report.wizard"
    _description = "create report wizard"
   
    listProduct = fields.Many2many('product.product',string='Liste De Produit', domain="[('sale_ok', '=', True)]")
    
    def action_print_report(self):
        return self.env.ref('pos_delete_orderline.report_ticket_print').report_action(self)
