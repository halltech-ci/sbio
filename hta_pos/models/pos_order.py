# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
class HtaPos(models.Model):
    _name = 'pos.order'
    _inherit = ['pos.order', 'mail.thread']
    _order = "order_date desc, id desc,name desc"
    
#     def _default_date_create(self):
#         for order in self:
#             order.date_order = order.create_date
    
    def _default_date_create(self):
        for order in self:
            if order.create_date:
                order.order_date = order.create_date
            elif order.date_order:
                order.order_date = order.date_order
            else:
                order.order_date = datetime.now()
                
        

    delivery_person = fields.Many2one(
        comodel_name="res.partner",
        string="Livreur",
    )

    date_delivery = fields.Datetime()
    order_date = fields.Datetime(string="Date commande",readonly=True, index=True,compute='_default_date_create')
    customer_Phone = fields.Char("Telephone",related='partner_id.phone', store=True)
    delivery_phone = fields.Char(related='delivery_person.phone', store=True)
    # date_order = fields.Datetime(string="Date commande",readonly=True, index=True,compute='_compute_date_create')
    user_return = fields.Many2one(
        comodel_name="res.users",
        string="Gestionnaire stock",
    )
    
#     @api.onchange('partner_id')
#     def _onchange_date_create(self):
#         now = datetime.now()
#         self.date_order = now
    

    # def _compute_date_create(self):
    #     for order in self:
    #         if order.create_date:
    #             order.date_order = order.create_date
            
    def assign_command_wizard(self):
    	#view_id = self.env.ref('point_of_sale.assign_command_wizard').id
    	context = self._context.copy()
    	return {
            'name':' Assigner au livreur',
            'type':'ir.actions.act_window',
            'view_mode': 'form',
            #'view_type': 'form',
            'res_model':'pos.assign.commands.wizard',
            #'res_id':self.env.ref('stock.picking').id,
            'target':'new',
        }
    
    def payment_wizard_order(self):
    	#view_id = self.env.ref('point_of_sale.payment_command_wizard').id
    	context = self._context.copy()
    	return {
            'name':'Passer au paiement',
            'type':'ir.actions.act_window',
            'view_mode': 'form',
            #'view_type': 'form',
            'res_model':'payment.after.delivery.wizard',
            #'res_id':self.env.ref('stock.picking').id,
            'target':'new',
        }
    
    def invoice_order_(self):
    	#view_id = self.env.ref('point_of_sale.payment_command_wizard').id
    	for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            if order.state != 'draft' or order.amount_paid >= pos_order.amount_total:
                order.action_pos_order_invoice()
            else:
                raise UserError(_("La commande Ref: "+str(pos_order.name) + " du client(e) "+str(pos_order.partner_id.name)+" n'est encore payée ou facturée"))
    

# class AssignPos(models.Model):
#     _name = 'assign.commands'
#     _description = "Assign Commande to Delivery Person"
#     _inherit = ["mail.thread", "mail.activity.mixin"]
#     _order = "id desc"

#     delivery_person = fields.Many2one(
#         comodel_name="res.partner",
#         string="Delivery Person",
#     )
#     purchase_lines = fields.Many2many(
#         comodel_name="pos.order",
#         string="Commands",
#         readonly=True,
#         copy=False,
#     )
#     date_delivery = fields.Datetime()


