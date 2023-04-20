from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

class CreateWizardReport(models.TransientModel):
    _name = "create.report.wizard"
    _description = "create report wizard"
   
    listProduct = fields.Many2many('product.product',string='Liste De Produit', domain="[('sale_ok', '=', True)]")
    
    def action_print_report(self):
        products = self.env['product.product'].browse(self.listProduct.ids)
        data = {
            "list_products": products,
            "form": self.read()[0]
        }
        selectproduct = data['form']['listProduct']
        listproduit = self.env['product.product'].search([('id','in',selectproduct)])
        liste_de_produit = []
        for item in listproduit:
            liste_de_produit.append({
                'name':item.partner_ref,
                'price':item.lst_price,
                'notice':item.notice_fields,
            })
        data["listproduit"] = liste_de_produit
        print("Data ==>>",data)
        return self.env.ref('pos_delete_orderline.report_ticket_print').report_action(self, data=data)