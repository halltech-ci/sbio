from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosPaymentCommands(models.TransientModel):
    _name = "payment.after.delivery.wizard"
    _description = "Payment After Payment"

    payment_method = fields.Many2one(
        comodel_name="pos.payment.method",
        string="Payment Method",
        required=True,
    )
    amount = fields.Float()
    

    @api.onchange('payment_method')
    def _onchange_partner(self):
        for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            self.amount = self.amount + order.amount_total
    
    def payment_after_orders(self):
        init_data = self.read()[0]
        for record in self._context.get('active_ids'):
            pos_order = self.env[self._context.get('active_model')].browse(record)
           
            pos_order.add_payment({
				'pos_order_id': pos_order.id,
				'amount': pos_order._get_rounded_amount(pos_order.amount_total),
				'payment_method_id': init_data['payment_method'][0],
                })
            if pos_order._is_pos_order_paid():
                pos_order.action_pos_order_paid()
                pos_order._compute_total_cost_in_real_time()
                #pos_order._create_order_picking()
                #return {'type': 'ir.actions.act_window_close'}


