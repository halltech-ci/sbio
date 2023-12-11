# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime, timedelta
import requests
import json


class PoOrder(models.Model):
    _inherit = "pos.order"

    is_return = fields.Boolean(default=False, tracking=True, string="Est un retour")
    delivery_status = fields.Selection(compute="_compute_delivery_status")
    montant_ca = fields.Monetary(compute="_compute_montant_ca")
    

    @api.depends("payment_ids", "amount_total")
    def _compute_montant_ca(self):
        for rec in self:
            rec.montant_ca = rec.amount_total 
            if not rec.payment_ids:
                rec.montant_ca = 0
            
    

    @api.depends("is_partial", "is_return", "delivery_person", "delivery_agent", "refunded_orders_count", "refunded_order_ids", "payment_ids")
    def _compute_delivery_status(self):
        for rec in self:
            rec.delivery_status = "draft"
            if rec.is_return:
                rec.delivery_status = "return"
            else:
                if rec.is_partial:
                    if rec.delivery_person or rec.delivery_agent:
                        rec.delivery_status = "delivery"
                else:
                    if rec.delivery_person or rec.delivery_agent :
                        rec.delivery_status = "invoiced"
                    if rec.refunded_orders_count and rec.refunded_order_ids:
                        rec.delivery_status = "refunded"
                    if not rec.delivery_person and not rec.delivery_agent:
                        rec.delivery_status = "direct"
                    
    def order_lines_writting(self):
        #pos_order=self.env['pos.order'].search([('id', '=', self.id)])
        lines = self.env['pos.order.line'].search([('order_id', '=', self.id)])
        if lines:
            for line in lines:
                new_vals = {
                    
                        'price_unit':0,
                        'price_subtotal':0,
                }
                line.write(new_vals)
                line._onchange_amount_line_all()
            self._onchange_amount_all()
        return True    

    def pos_orders_return(self):
        for order in self:
            if order.payment_ids:
                order.pos_order_refund()
                order.write({"is_return": True})
            else:
                order.action_return_without_refund()
                lines = self.env['pos.order.line'].search([('order_id', '=', order.id)])
                if lines:
                    for line in lines:
                        new_vals = {
                                'price_unit':0,
                                'price_subtotal':0,
                            }
                        line.update(new_vals)
                        line._onchange_amount_line_all()
                order._onchange_amount_all()
                order.write({"is_return": True, "state": "cancel"})

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
        pickings = self.env['stock.picking'].search([('pos_order_id', '=', self.id), ("state", "=", "done")])
        if len(pickings) == 1:
            stock_return = self.env['stock.return.picking'].create({'picking_id':pickings.id})
            stock_return._onchange_picking_id()
            picking_id = stock_return.create_returns().get("res_id")
            picking = self.env["stock.picking"].browse(picking_id)
            picking.action_set_quantities_to_reservation()
            picking.button_validate()
            #self.update({"delivery_status": "return"})
            return picking
        else:
            raise UserError(_("Vous ne pouvez pas traiter plusieurs livraisons."))
            
    
    def audit_valid(self):
        for record in self._context.get('active_ids'):
            order = self.env[self._context.get('active_model')].browse(record)
            order_lines = order.lines
            if order.is_return :
                for rs in order_lines:
                    line = {
                            "price_unit": 0,
                            "price_subtotal": 0,
                            'price_subtotal_incl': 0,
                            }
                    rs.write(line)
                    rs._onchange_amount_line_all()
                order._onchange_amount_all()
                order.write({'audit':'valide','date_audit': datetime.now(),'audit_valideur':self.env.user})
            else:
                for rs in order_lines:
                    if 'ivraison' in str(rs.full_product_name):
                        line = {
                            "price_unit": 0,
                            "price_subtotal": 0,
                            'price_subtotal_incl': 0,
                            
                            }
                        rs.write(line)
                    rs._onchange_amount_line_all()
                order._onchange_amount_all()
                order.write({'audit':'valide','date_audit': datetime.now(),'audit_valideur':self.env.user})
                