# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _name = 'report.product.free'
    _description = "Produit gratuit"
    
    date_start = fields.Date(string='Entre', required=True, default=fields.Date.today)
    date_end = fields.Date(string='Au', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    product_id = fields.Many2many('product.product', string="Article")
    

    def get_report(self):
        data = {
            'model':'report.product.free',
            'form': self.read()[0]
        }
        selectproduct = data['form']['product_id']
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        liste_de_produit = []
        if date_start and date_end:
            listproduit = self.env['pos.order.line'].search([('order_id.state','!=','return'),('create_date','>=',date_start),('create_date','<=',date_end),('full_product_name','not ilike','ivraison'),('price_subtotal','=',0.0),('full_product_name','not ilike','remise')])
        else:
            listproduit = self.env['pos.order.line'].search([('order_id.state','!=','return'),('full_product_name','not ilike','ivraison'),('price_subtotal','=',0.0),('full_product_name','not ilike','remise')])
        
        for item in listproduit:
            liste_de_produit.append({
                'name':item.full_product_name,
                'quantite':item.qty,
                'partner':item.order_id.partner_id.name,
                'phone':item.order_id.partner_id.phone,
                'commercial':item.order_id.user_id.name,
                'date':item.order_id.order_date,
            })
        listproduit = self.env['pos.order.line'].search([('order_id.state','!=','return'),('full_product_name','not ilike','ivraison'),('order_id.amount_total','=',0.0),('full_product_name','not ilike','remise'),('create_date','>=',date_start),('create_date','<=',date_end)])
        for item in listproduit:
            liste_de_produit.append({
                'name':item.full_product_name,
                'quantite':item.qty,
                'partner':item.order_id.partner_id.name,
                'phone':item.order_id.partner_id.phone,
                'commercial':item.order_id.user_id.name,
                'date':item.order_id.order_date,
            })
        data["listproduit"] = liste_de_produit
        print("Data ==>>",data)
        return self.env.ref('hta_pos.generate_product_free_xlsx_report').report_action(self, data=data)
