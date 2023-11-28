from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PosAssignCommands(models.TransientModel):
    _name = "pos.assign.commands.wizard"
    _description = "Assign Commands Pos"

    delivery_agent = fields.Many2one(
        comodel_name="delivery.agent",
        string="Delivery Person",
        #required=True,
    )
    delivery_person = fields.Many2one("res.partner")
    date_delivery = fields.Date(string='Date Livraison', required=True, default=fields.Date.today)
    
#     state = fields.Selection(selection_add=[('')])
    
    def print_order_assigner(self):
        docs = []
        
        for record in self._context.get('active_ids'):
            pos_order = self.env[self._context.get('active_model')].browse(record)
            line_docs = []
            for rs in pos_order.lines:
                line_docs.append({
                    'full_product_name':rs.full_product_name,
                    'qty':rs.qty,
                })
            docs.append({
                    'pos_reference':pos_order.pos_reference,
                    'pos_order_date':self.date_delivery,
                    'amount_total': pos_order.amount_total,
                    'line_docs':line_docs,
                })
        data = {
                    'model':'pos.assign.commands.wizard',
                    'form': self.read()[0],
                    'orders':docs,
                    }
        return self.env.ref('hta_pos.pos_report_assign_order').with_context(landscape=True).report_action(self, data=data)
    
    def assign_delivery_orders(self):
        docs = []
        for record in self._context.get('active_ids'):
            pos_order = self.env[self._context.get('active_model')].browse(record)
            line_docs = []
            pickings = self.env["pos.order"].browse(record).picking_ids
            if len(pickings) == 1:
                picking = pickings
            if picking.state == "confirmed":
                picking.action_assign()
                picking.action_set_quantities_to_reservation()
                picking.button_validate()
                picking._action_done()
            if picking.state == "assign":
                picking.action_set_quantities_to_reservation()
                picking.button_validate()
                picking._action_done()
            for rs in pos_order.lines:
                line_docs.append({
                    'full_product_name':rs.full_product_name,
                    'qty':rs.qty,
                })
            docs.append ({
                'pos_order': pos_order,
                'pos_reference':pos_order.pos_reference,
                'pos_order_date':self.date_delivery,
                'amount_total': pos_order.amount_total,
                'line_docs':line_docs,
            })
            '''if pos_order.delivery_agent:
                raise UserError(_("LES COMMANDES SONT DEJA ASSIGNER"))
            else:
            '''    
            pos_order.delivery_agent = self.delivery_agent
            pos_order.date_delivery = self.date_delivery
            pos_order.delivery_status = 'delivery'
                
        data = {
                    'model':'pos.assign.commands.wizard',
                    'form': self.read()[0],
                    'orders':docs,
                    }
        return self.env.ref('hta_pos.pos_report_assign_order').with_context(landscape=True).report_action(self, data=data)


