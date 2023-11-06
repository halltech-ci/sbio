# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PoOrder(models.Model):
    _inherit = "pos.order"

    is_return = fields.Boolean(default=False)

    @api.depends("state", "delivery_person", "is_return")
    def _compute_delivery_status(self):
        for rec in self:
            rec.delivery_status = "draft"
            if rec.is_return:
                rec.delivery_status = "return"
            if rec.delivery_person and rec.state in ["paid", "invoiced", "post"]:
                rec.delivery_status = "invoiced"
            if not rec.delivery_person and rec.state in ["paid", "invoiced", "done"]:
                rec.delivery_status = "direct"


    def pos_orders_return(self):
        for order in self:
            if order.payment_ids:
                order.pos_order_refund()
                order.write({"is_return": True})
            else:
                order.action_return_without_refund()
                order.write({"is_return": True})

    def pos_order_refund(self):
        refund_orders = self.env['pos.order']
        for order in self:
            current_session = order.session_id
            if not current_session:
                raise UserError(_('To return product(s), you need to open a session in the POS %s', order.session_id.config_id.display_name))
            refund_order = order.copy(order._prepare_refund_values(current_session))
            for line in order.lines:
                PosOrderLineLot = self.env['pos.pack.operation.lot']
                for pack_lot in line.pack_lot_ids:
                    PosOrderLineLot += pack_lot.copy()
                line.copy(line._prepare_refund_data(refund_order, PosOrderLineLot))
            refund_orders |= refund_order

        return {
            'name': _('Return Products'),
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id': refund_orders.ids[0],
            'view_id': False,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        

    def action_return_without_refund(self):
        pickings = self.env['stock.picking'].search([('pos_order_id', '=', self.id), ("state", "=", "assigned")])
        if len(pickings) == 1:
            stock_return = self.env['stock.return.picking'].create({'picking_id':picking_id.id})
            stock_return._onchange_picking_id()
            picking_id = stock_return.create_returns().get("res_id")
            picking = self.env["stock.picking"].browse(picking_id)
            picking.action_set_quantities_to_reservation()
            picking.button_validate()
            #self.update({"delivery_status": "return"})
            return picking
        else:
            raise UserError(_("Vous ne pouvez pas traiter plusieurs livraisons."))
            
    
    