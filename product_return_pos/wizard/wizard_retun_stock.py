
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round




class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"