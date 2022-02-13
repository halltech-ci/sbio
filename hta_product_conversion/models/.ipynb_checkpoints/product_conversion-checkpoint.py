# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
import time

class ProductConversion(models.Model):
    _name = "product.conversion"
    _description = "Model for product unit of mesure conversion"
    
    name = fields.Text(string="Name", default='/')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft')
    src_product_id = fields.Many2one('product.product', string='Product')
    src_uom = fields.Many2one('uom.uom', string="Unit of measure")
    src_lot = fields.Many2one('stock.production.lot', string='Source Lot')
    src_product_tracking = fields.Selection(related='src_product_id.tracking', readonly=True)
    from_location = fields.Many2one('stock.location', string='Source Location')
    qty_to_convert = fields.Float(string="Quantity To Convert")
    conversion_line = fields.One2many('product.conversion.line', 'conversion_id', string='Conversion Line')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.conversion'))
    date = fields.Date(string='Date', index=True, default=time.strftime('%Y-%m-%d'))
    
    
    
class ProductConversionLinem(models.Model):
    _name = "product.conversion.line"
    _description = "Line for product conversion"
    
    conversion_id = fields.Many2one('product.conversion', string='Conversion id')
    conversion_ratio = fields.Float(string='Conversion Ratio')
    dest_product_id = fields.Many2one('product.product', string="Product")
    dest_uom = fields.Many2one('uom.uom', string="Unit of measure")
    dest_lot = fields.Many2one('stock.production.lot', string='Destination Lot')
    to_location = fields.Many2one('stock.location', string='Destination Location')
    converted_qty = fields.Float(string='Converted Quantity')
    dest_product_tracking = fields.Selection(related='dest_product_id.tracking', readonly=True)
    allocate_quantity = fields.Float(string='Allocate Quantity', digits='Product Unit of Measure')
    company_id = fields.Many2one(related='conversion_id.company_id', string='Company', store=True, readonly=True)
    
    
class ProductProduct(models.Model):
    _inherit = "product.product"

    conversion_line = fields.One2many('product.line', 'prod_id', string='Conversion')
    #duplicate_product_check = fields.Boolean(string='Duplicate Product Check', compute="_compute_check_duplicate_convertible_product")
    
    """
    @api.depends('conversion_line.convertible_product')
    def _compute_check_duplicate_convertible_product(self):
        lst = []
        self.duplicate_product_check = False
        for conversion in self.conversion_line:
            if conversion.convertible_product not in lst:
                lst.append(conversion.convertible_product)
            else:
                raise UserError(_('Conversion Ratio for ' + str(conversion.convertible_product.name) + ' has already been set'))
        self.duplicate_product_check = True
    """


class ProductLine(models.Model):
    _name = "product.line"
    _description = "product conversion product line"

    prod_id = fields.Many2one('product.product', string="Prod id")
    conversion_ratio = fields.Float(string='Conversion Ratio')
    convertible_product = fields.Many2one('product.product', string='Convertible Product')
    uom_id = fields.Many2one('uom.uom', string="UOM")

    @api.onchange('convertible_product')
    def onchange_uom(self):
        if self.convertible_product:
            self.uom_id = self.convertible_product.uom_id.id
        return {}
    