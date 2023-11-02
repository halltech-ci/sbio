# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PoOrder(models.Model):
    _inherit = "pos.order"


    def pos_orders_return(self):
        for record in self._context.get("active_ids"):
            order = self.env["pos.order"].browse(record)



    def pos_action_return(self):
        picking_id = self.env['stock.picking'].search([('pos_order_id', '=', self.id), ("state", "=", "assigned")])
        if len(picking_id) == 1:
            stock_return = self.env['stock.return.picking'].create({'picking_id':picking_id.id})
            stock_return._onchange_picking_id()
            
        