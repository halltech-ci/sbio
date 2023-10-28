# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = "pos.order"


    def _create_order_draft_picking(self):
        self.ensure_one()
        if self.to_ship:
            self.lines._launch_stock_rule_from_pos_order_lines()
        else:
            if self._should_create_picking_real_time():
                picking_type = self.config_id.picking_type_id
                if self.partner_id.property_stock_customer:
                    destination_id = self.partner_id.property_stock_customer.id
                elif not picking_type or not picking_type.default_location_dest_id:
                    destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
                else:
                    destination_id = picking_type.default_location_dest_id.id

                pickings = self.env['stock.picking']._create_draft_picking_from_pos_order_lines(destination_id, self.lines, picking_type, self.partner_id)
                pickings.write({'pos_session_id': self.session_id.id, 'pos_order_id': self.id, 'origin': self.name})


    def action_pos_order_paid(self):
        self.ensure_one()
        if not self.is_partial:
            return super(PosOrder, self).action_pos_order_paid()
        if self.is_partial:
            if self._is_pos_order_paid():
                self.write({'state': 'paid'})
                if self.picking_ids:
                    return True
                else :
                    return self._create_order_picking()
            else:
                if not self.picking_ids :
                    return self._create_order_draft_picking()
                else:
                    return False
