
from odoo import models, fields, api

class HtaPos(models.Model):
    _inherit = 'stock.picking'
    

    def wizard_stock_return_picking(self):
    	view_id = self.env.ref('stock.view_stock_return_picking_form').id
    	context = self._context.copy()
    	return {
            'name':'Reverse Transfer',
            'type':'ir.actions.act_window',
            'view_mode': 'form',
            #'view_type': 'form',
            'res_model':'stock.return.picking',
            #'res_id':self.env.ref('stock.picking').id,
            'target':'new',
        }

