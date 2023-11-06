# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _
from itertools import groupby
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class PosPackOrderLine(models.Model):
    _name = "pos.pack.order.line"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product', string='Product')
    price_unit = fields.Float(string='Unit Price')
    qty = fields.Float(string='Quantity')
    wk_order_id = fields.Many2one('pos.order', string='Order Ref', ondelete='cascade')
    
class StockPicking(models.Model):
    _inherit='stock.picking'

    def _create_move_from_pos_order_lines(self, lines):
        self.ensure_one()
        lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
        for product, lines in lines_by_product:
            order_lines = self.env['pos.order.line'].concat(*lines)
            first_line = order_lines[0]

            # -------- Picking for Product Pack Items ---------
            if order_lines and order_lines.product_id.is_pack and order_lines.product_id.pack_stock_management != 'decrmnt_pack':
                for wk_pack_product in order_lines.product_id.wk_product_pack.filtered(lambda l: l.product_id.type in ['product', 'consu']):
                    current_move = self.env['stock.move'].create(
                                                            {
                                                                'name': wk_pack_product.product_id.name,
                                                                'product_uom': wk_pack_product.product_id.uom_id.id,
                                                                'picking_id': self.id,
                                                                'picking_type_id': self.picking_type_id.id,
                                                                'product_id': wk_pack_product.product_id.id,
                                                                'product_uom_qty': abs(sum(order_lines.mapped('qty'))),
                                                                'state': 'draft',
                                                                'location_id': self.location_id.id,
                                                                'location_dest_id': self.location_dest_id.id,
                                                                'company_id': self.company_id.id,
                                                            }
                                                        )
                    confirmed_moves = current_move._action_confirm()
                    for move in confirmed_moves:
                        move.quantity_done = move.product_uom_qty

            if order_lines and order_lines.product_id.is_pack and order_lines.product_id.pack_stock_management == 'decrmnt_products':
                return False

            current_move = self.env['stock.move'].create(
                self._prepare_stock_move_vals(first_line, order_lines)
            )
            confirmed_moves = current_move._action_confirm()
            for move in confirmed_moves:
                if first_line.product_id == move.product_id and first_line.product_id.tracking != 'none':
                    if self.picking_type_id.use_existing_lots or self.picking_type_id.use_create_lots:
                        for line in order_lines:
                            sum_of_lots = 0
                            for lot in line.pack_lot_ids.filtered(lambda l: l.lot_name):
                                if line.product_id.tracking == 'serial':
                                    qty = 1
                                else:
                                    qty = abs(line.qty)
                                ml_vals = move._prepare_move_line_vals()
                                ml_vals.update({'qty_done':qty})
                                if self.picking_type_id.use_existing_lots:
                                    existing_lot = self.env['stock.production.lot'].search([
                                        ('company_id', '=', self.company_id.id),
                                        ('product_id', '=', line.product_id.id),
                                        ('name', '=', lot.lot_name)
                                    ])
                                    if not existing_lot and self.picking_type_id.use_create_lots:
                                        existing_lot = self.env['stock.production.lot'].create({
                                            'company_id': self.company_id.id,
                                            'product_id': line.product_id.id,
                                            'name': lot.lot_name,
                                        })
                                    ml_vals.update({
                                        'lot_id': existing_lot.id,
                                    })
                                else:
                                    ml_vals.update({
                                        'lot_name': lot.lot_name,
                                    })
                                self.env['stock.move.line'].create(ml_vals)
                                sum_of_lots += qty
                            if abs(line.qty) != sum_of_lots:
                                difference_qty = abs(line.qty) - sum_of_lots
                                ml_vals = current_move._prepare_move_line_vals()
                                if line.product_id.tracking == 'serial':
                                    ml_vals.update({'qty_done': 1})
                                    for i in range(int(difference_qty)):
                                        self.env['stock.move.line'].create(ml_vals)
                                else:
                                    ml_vals.update({'qty_done': difference_qty})
                                    self.env['stock.move.line'].create(ml_vals)
                    else:
                        move._action_assign()
                        sum_of_lots = 0
                        for move_line in move.move_line_ids:
                            move_line.qty_done = move_line.product_uom_qty
                            sum_of_lots += move_line.product_uom_qty
                        if float_compare(move.product_uom_qty, move.quantity_done, precision_rounding=move.product_uom.rounding) > 0:
                            remaining_qty = move.product_uom_qty - move.quantity_done
                            ml_vals = move._prepare_move_line_vals()
                            ml_vals.update({'qty_done':remaining_qty})
                            self.env['stock.move.line'].create(ml_vals)

                else:
                    move.quantity_done = move.product_uom_qty

class PosOrder(models.Model):
    _inherit = 'pos.order'

    wk_product_pack_lines = fields.One2many('pos.pack.order.line', 'wk_order_id', string='Order Lines')
    
    def create_picking(self):
        """Create a picking for each order and validate it."""
        Picking = self.env['stock.picking']
        Move = self.env['stock.move']
        StockWarehouse = self.env['stock.warehouse']
        for order in self:
            address = order.partner_id.address_get(['delivery']) or {}
            picking_type = order.picking_type_id
            return_pick_type = order.picking_type_id.return_picking_type_id or order.picking_type_id
            order_picking = Picking
            return_picking = Picking
            moves = Move
            location_id = picking_type.default_location_src_id.id
            if order.partner_id:
                destination_id = order.partner_id.property_stock_customer.id
            else:
                if (not picking_type) or (not picking_type.default_location_dest_id):
                    customerloc, supplierloc = StockWarehouse._get_partner_locations()
                    destination_id = customerloc.id
                else:
                    destination_id = picking_type.default_location_dest_id.id

            if picking_type:
                message = _("This transfer has been created from the point of sale session: <a href=# data-oe-model=pos.order data-oe-id=%d>%s</a>") % (order.id, order.name)
                picking_vals = {
                    'origin': order.name,
                    'partner_id': address.get('delivery', False),
                    'date_done': order.date_order,
                    'picking_type_id': picking_type.id,
                    'company_id': order.company_id.id,
                    'move_type': 'direct',
                    'note': order.note or "",
                    'location_id': location_id,
                    'location_dest_id': destination_id,
                }
                pos_qty = any([x.qty >= 0 for x in order.lines])
                if pos_qty:
                    order_picking = Picking.create(picking_vals.copy())
                    order_picking.message_post(body=message)
                neg_qty = any([x.qty < 0 for x in order.lines])
                if neg_qty:
                    return_vals = picking_vals.copy()
                    return_vals.update({
                        'location_id': destination_id,
                        'location_dest_id': return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        'picking_type_id': return_pick_type.id
                    })
                    return_picking = Picking.create(return_vals)
                    return_picking.message_post(body=message)

            for line in order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu']  or l.product_id.is_pack):
                if line.product_id.is_pack and line.product_id.pack_stock_management != 'decrmnt_pack':
                    for wk_pack_product in line.product_id.wk_product_pack.filtered(lambda l: l.product_id.type in ['product', 'consu']):
                        pack_qty = (wk_pack_product.product_quantity) *line.qty
                        moves |= Move.create({
                            'name': wk_pack_product.product_id.name,
                            'product_uom': wk_pack_product.product_id.uom_id.id,
                            'picking_id': order_picking.id if pack_qty >= 0 else return_picking.id,
                            'picking_type_id': picking_type.id if pack_qty >= 0 else return_pick_type.id,
                            'product_id': wk_pack_product.product_id.id,
                            'product_uom_qty': abs(pack_qty),
                            'state': 'draft',
                            'location_id': location_id if pack_qty >= 0 else destination_id,
                            'location_dest_id': destination_id if pack_qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                        })

                if(line.product_id.type != 'service'):
                    moves |= Move.create({
                        'name': line.name,
                        'product_uom': line.product_id.uom_id.id,
                        'picking_id': order_picking.id if line.qty >= 0 else return_picking.id,
                        'picking_type_id': picking_type.id if line.qty >= 0 else return_pick_type.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': abs(line.qty),
                        'state': 'draft',
                        'location_id': location_id if line.qty >= 0 else destination_id,
                        'location_dest_id': destination_id if line.qty >= 0 else return_pick_type != picking_type and return_pick_type.default_location_dest_id.id or location_id,
                    })

            # prefer associating the regular order picking, not the return
            order.write({'picking_id': order_picking.id or return_picking.id})

            if return_picking:
                order._force_picking_done(return_picking)
            if order_picking:
                order._force_picking_done(order_picking)

            # when the pos.config has no picking_type_id set only the moves will be created
            if moves and not return_picking and not order_picking:
                moves._action_assign()
                moves.filtered(lambda m: m.state in ['confirmed', 'waiting']).force_assign()
                moves.filtered(lambda m: m.product_id.tracking == 'none')._action_done()

        return True

    