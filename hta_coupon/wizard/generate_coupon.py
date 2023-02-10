# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WizardCoupon(models.TransientModel):
    _name = 'coupon.coupon.wizard'
    _description = "Generer Coupon"
    
    
    nom_coupon = fields.Char(string='Nom Coupon',required=True)
    filter_recompense = fields.Selection([('remise', 'Remise'), ('produit', 'Produit Gratuit')], string='Filtre Recompense',default='remise',required=True)
    filter_client = fields.Selection([('date', 'Par Date'),('client', 'Pour un client Precis')], string='Filtre Client',default='date',required=True)
    
    pourcentage = fields.Float(string='Pourcentage')
    produit = fields.Many2one('product.product',string='Produit')
    
    partner_id = fields.Many2one('res.partner',string='CLIENT')
    date_start = fields.Date(string='Date Debut', default=fields.Date.today)
    date_end = fields.Date(string='Date Fin', default=fields.Date.today)
    amount_min = fields.Float(string='Montant Min')
    amount_max = fields.Float(string='Montant Max')
    
    def program_coupon(self,name, pourcentage):
        programme = {
                    'name': name,
                    'active': True,
                    'program_type':'coupon_program',
                    # 'company_id': self.env.company,
                    'promo_applicability': 'on_current_order',
                    'validity_duration':60,
                    'rule_minimum_amount_tax_inclusion':'tax_excluded',
                    'reward_type':'discount',
                    'discount_type':'percentage',
                    'discount_percentage':pourcentage,
                    # 'rule_id':rule.id,
                    # 'reward_id':reward.id,
                    }
            
        program_coupon = self.env['coupon.program'].sudo().create(programme)
        
        return program_coupon
    

    def generate_coupon(self):
        name = self.nom_coupon
        filtre_recom = self.filter_recompense
        filtre_cl = self.filter_client
        pourcentage = self.pourcentage
        produit = self.produit
        partner_id = self.partner_id
        date_start = self.date_start
        date_end = self.date_end
        amount_min = self.amount_min
        amount_max = self.amount_max
        pos_list = self.env['pos.order'].search([])
        res_partner = self.env['res.partner'].search([])
        if self.filter_recompense == "remise" and self.filter_client == "date":
            pourcentage = self.pourcentage
#             coupon_rule = {
#                     'rule_minimum_amount_tax_inclusion':'tax_excluded',
#                     }
#             rule = self.env['coupon.rule'].create(coupon_rule)
            
#             coupon_reward = {
#                     'reward_type':'discount',
#                     'discount_type':'percentage',
#                     'discount_percentage':pourcentage,
#                     }
#             reward = self.env['coupon.reward'].create(coupon_reward)
#             reward.name_get()
#             print(reward)
            program = self.program_coupon(name, pourcentage)
            for res_p in res_partner:
                id_partner = res_p.id
                partner_name = res_p.name
                partner_phone = res_p.phone
                montant = 0
                pos_list = self.env['pos.order'].search([('partner_id','=',id_partner),('date_order','>=',date_start),('date_order','<=',date_end)])
                for line in pos_list:
                    montant = montant + line.amount_paid
                if (self.amount_min > 0 and self.amount_min <= montant < self.amount_max):
                    coupon = {
                        'program_id':program.id,
                        'partner_id':id_partner,
                        'state':'new',
                    }
                    program_coupon = self.env["coupon.coupon"].sudo().create(coupon)
                    program_coupon.sudo()._generate_code()
                
        elif (filtre_recom == "remise" and filtre_cl == "client"):
            pourcentage = self.pourcentage
            partner_id = self.partner_id
            pos_list = self.env['pos.order'].search([('partner_id','=',partner_id),('date_order','>=',date_start),('date_order','<=',date_end)])
            for line in pos_list:
                montant = montant + line.amount_paid
                    