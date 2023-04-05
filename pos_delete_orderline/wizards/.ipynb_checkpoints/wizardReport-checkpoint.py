
from odoo import api, fields, models


class CreateWizardReport(models.TransientModel):
    _name = "create.report.wizard"
    _description = "create report wizard"
    
    produits = fields.Many2many('product.product')
    
    @api.model
    def _get_produits_selection(self):
        produits = self.env['product.product'].search([])
        return sorted([(p.id, p.name) for p in produits])
   
    listProduct =  fields.Selection(selection=_get_produits_selection, string='Liste De Produit')
    
    def action_print_report (self):
        print("Yo le sang tu connais ou quoi")