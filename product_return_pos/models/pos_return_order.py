# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Anusha P P (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import models, api, fields, _
from odoo.tools.float_utils import float_round

class PosOrderReturn(models.Model):
    _inherit = 'pos.order'
    state = fields.Selection(selection_add=[('draft','Livraison'),('paid',),('return','Retour')])
    lines = fields.One2many('pos.order.line', 'order_id', string='Order Lines', states={'draft': [('readonly', False)],'return': [('readonly', False)]}, readonly=True, copy=True)

    def order_lines_writting(self):
        #pos_order=self.env['pos.order'].search([('id', '=', self.id)])
        lines = self.env['pos.order.line'].search([('order_id', '=', self.id)])
        if lines:
            for line in lines:
                new_vals = {
                        
                        'price_subtotal':0,
                }
                line.write(new_vals)
        self.write({'amount_total':0,})
        return True
    

    def display_form_return_stock(self, picking_id):  
        view = self.env.ref('stock.act_stock_return_picking',False).id
        wiz = self.env['stock.return.picking'].create({'picking_id':picking_id.id})
        move_dest_exists = False
        product_return_moves = [(5,)]
        line_fields = [f for f in self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env['stock.return.picking.line'].default_get(line_fields)
        for move in picking_id.move_lines:
            if move.state == 'cancel':
                continue
            if move.scrapped:
                continue
            if move.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(self._prepare_stock_return_picking_line_vals_from_move(move))
            product_return_moves.append((0, 0, product_return_moves_data))
        if picking_id and not product_return_moves:
            raise UserError(_("No products to return (only lines in Done state and not fully returned yet can be returned)."))
        
        location_id = picking_id.location_id.id
        if picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
            location_id = picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id
        wiz.write({
                'product_return_moves':product_return_moves,
                'parent_location_id': picking_id.picking_type_id.warehouse_id and picking_id.picking_type_id.warehouse_id.view_location_id.id or picking_id.location_id.location_id.id,
            'original_location_id': picking_id.location_id.id,
            
            'location_id': location_id
            })
            
        return {
                'name': 'Retour',
                'type': 'ir.actions.act_window',
                #'view_id': view.id,
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'res_model': 'stock.return.picking',
                #'views': [(view, 'form')],
                'target': 'new',
               }


    def retunr_stock_picking(self):
        lines = self.env['stock.picking'].search([('pos_order_id', '=', self.id)])
        
        if len(lines)<2:
            return self.display_form_return_stock(lines)
        else:
            pass
    

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        quantity = stock_move.product_qty
        for move in stock_move.move_dest_ids:
            if move.origin_returned_move_id and move.origin_returned_move_id != stock_move:
                continue
            if move.state in ('partially_available', 'assigned'):
                quantity -= sum(move.move_line_ids.mapped('product_qty'))
            elif move.state in ('done'):
                quantity -= move.product_qty
        quantity = float_round(quantity, precision_rounding=stock_move.product_id.uom_id.rounding)
        return {
            'product_id': stock_move.product_id.id,
            'quantity': quantity,
            'move_id': stock_move.id,
            'uom_id': stock_move.product_id.uom_id.id,
        }


    
    def buuton_retunr_order(self):
        retour_stock = self.retunr_stock_picking()
        self.order_lines_writting()
        self.state = "return"
        
    def buuton_state_new(self):
        lines = self.env['pos.order.line'].search([('order_id', '=', self.id)])
        if lines:
            for line in lines:
                line._onchange_amount_line_all()

        self._onchange_amount_all()
        self.state = "draft"
    
#     def _order_fields(self, ui_order):
#         order = super(PosOrderReturn, self)._order_fields(ui_order)
#         if 'return_ref' in ui_order.keys() and ui_order['return_ref']:
#             order['return_ref'] = ui_order['return_ref']
#             parent_order = self.search([('pos_reference', '=', ui_order['return_ref'])], limit=1)

#             updated_lines = ui_order['lines']
#             ret = 0
#             qty = 0
#             for uptd in updated_lines:
#                 line = self.env['pos.order.line'].search([('order_id', '=', parent_order.id),
#                                                            ('id', '=', uptd[2]['line_id'])], limit=1)
#                 if line:
#                     line.returned_qty += -(uptd[2]['qty'])
#             for line in parent_order.lines:
#                 qty += line.qty
#                 ret += line.returned_qty
#             if qty-ret == 0:
#                 if parent_order:
#                     parent_order.return_status = 'fully_return'
#                     print(parent_order.return_status)
#             elif ret:
#                 if qty > ret:
#                     if parent_order:
#                         parent_order.return_status = 'partialy_return'

#         return order


# class PosOrderLineReturn(models.Model):
#     _inherit = 'pos.order.line'

#     returned_qty = fields.Integer(string='Returned Qty', readonly=True)
