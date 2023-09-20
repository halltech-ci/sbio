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
        amount = 0
        for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            amount += order.amount_total
        self.amount = amount
    
    def payment_after_orders(self):
        init_data = self.read()[0]
        for record in self._context.get('active_ids'):
            pos_order = self.env[self._context.get('active_model')].browse(record)
            order_lines = pos_order.lines
            # if pos_order.amount_paid >= pos_order.amount_total and pos_order.state in ['invoiced','done','paid']:
            if pos_order.amount_paid >= pos_order.amount_total:
                 raise UserError(_("La commande Ref: "+str(pos_order.name) + " du client(e) "+str(pos_order.partner_id.name)+" a été  déjà Payée ou Facturée"))
            
            elif pos_order.state not in ['invoiced','done','paid'] and pos_order.amount_paid >= pos_order.amount_total:
                if pos_order._is_pos_order_paid():
                    pos_order.action_pos_order_paid()
                    pos_order.write({
                        'is_partial' : False,
                        })
                    pos_order._compute_total_cost_in_real_time()
                    pos_order.action_pos_order_invoice()
                else:
                    pos_order.state = 'invoiced'
            else:
                for rs in order_lines:
                    if 'ivraison' in rs.full_product_name:
                        line = {
                            "price_unit": 0,
                            "price_subtotal": 0,
                            'price_subtotal_incl': 0,
                        }

                        rs.write(line)
                    rs._onchange_amount_line_all()

    #             pos_order._onchange_amount_line_all()
                pos_order._onchange_amount_all()

                pos_order.add_payment({
                    'pos_order_id': pos_order.id,
                    'amount': pos_order._get_rounded_amount(pos_order.amount_total),
                    'payment_method_id': init_data['payment_method'][0],
                    })
                if pos_order._is_pos_order_paid():
                    pos_order.action_pos_order_paid()
                    pos_order.write({
                        'is_partial' : False,
                        })
                    pos_order._compute_total_cost_in_real_time()
                    pos_order.action_pos_order_invoice()

                bank_statment = self.env['account.bank.statement']
                if pos_order.session_id.state == 'closed':
                    name_statement = str(pos_order.session_id.name)+"/1"
                    if not bank_statment.search([('name','=',name_statement)]):
                        journal_id = pos_order.payment_ids[:1].payment_method_id.journal_id
                        value = []
                        lines = (0, 0, {
                            "payment_ref": pos_order.session_id.name,
                            "partner_id": pos_order.partner_id.id,
                            'amount': pos_order.amount_paid,
                        })
                        value.append(lines)
                        bank_statment.create({'name':name_statement,'date':pos_order.session_id.start_at,'journal_id':journal_id.id,
                                              'company_id':pos_order.company_id.id,
                                             'line_ids':value})
                    else:
                        line_bank_statement = bank_statment.search([('name','=',name_statement)])[:1]

                        value = []
                        lines = (0, 0, {
                            "payment_ref": pos_order.session_id.name,
                            "partner_id": pos_order.partner_id.id,
                            'amount': pos_order.amount_paid,
                        })
                        value.append(lines)
                        line_bank_statement.write({'line_ids':value})
                
                #pos_order._create_order_picking()
                #return {'type': 'ir.actions.act_window_close'}
                
        


