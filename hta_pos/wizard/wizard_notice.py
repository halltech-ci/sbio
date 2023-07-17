# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _name = 'report.notice.wizard'
    _description = "Notice"
    
    product_id = fields.Many2many('product.notice', string="Article")
    

    def get_report(self):
        data = {
            'model':'report.notice.wizard',
            'form': self.read()[0]
        }
        selectproduct = data['form']['product_id']
        listproduit = self.env['product.notice'].search([('id','in',selectproduct)])
        liste_de_produit = []
        for item in listproduit:
            liste_de_produit.append({
                'name':item.name,
                'price':item.price,
                'notice':item.notice,
            })
        data["listproduit"] = liste_de_produit
        print("Data ==>>",data)
        return self.env.ref('hta_pos.report_ticket_notice').report_action(self, data=data)
