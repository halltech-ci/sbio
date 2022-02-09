# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
import time
#from odoo.addons import decimal_precision as dp


class ProductConversion(models.Model):
    _name = "product.conversion"
    _description = "Product Conversion"

    name = fields.Text(string="Name", default='/')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft')
    src_product_id = fields.Many2one('product.product', string='Product')
    src_uom = fields.Many2one('uom.uom', string="Unit of measure")
    src_lot = fields.Many2one('stock.production.lot', string='Source Lot')
    src_product_tracking = fields.Selection(related='src_product_id.tracking', readonly=True)
    from_location = fields.Many2one('stock.location', string='Source Location')
    qty_to_convert = fields.Float(string="Quantity To Convert")
    conversion_line = fields.One2many('product.conversion.line', 'conversion_id', string='Conversion Line')
    product_ids = fields.Many2many('product.product', string='product ids', compute="_compute_store_convertible_products")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.conversion'))
    date = fields.Date(string='Date', index=True, default=time.strftime('%Y-%m-%d'))

    @api.onchange('src_product_id', 'qty_to_convert', 'src_lot', 'from_location')
    def onchange_product_uom(self):
        if self.src_product_id:
            self.src_uom = self.src_product_id.uom_id.id
            for ratio in self.src_product_id.conversion_line:
                if not ratio.convertible_product.id:
                    raise UserError(str(self.src_product_id.name) + ' has no convertible product. Kindly map a Convertible Product')
        if not self.src_product_id:
            self.src_uom = False
        if self.src_lot:
            check_lot_qty = self.env['stock.quant']._get_available_quantity(self.src_product_id, self.from_location, self.src_lot)
            if check_lot_qty < self.qty_to_convert:
                raise UserError(_('Given Quantity to convert for the product ' + str(self.src_product_id.name) + ' is not available in the lot ' + str(self.src_lot.name)))
        else:
            check_product_qty = self.env['stock.quant']._get_available_quantity(self.src_product_id, self.from_location)
            if check_product_qty < self.qty_to_convert:
                raise UserError(_('Given Quantity to convert for the product ' + str(self.src_product_id.name) + ' is not available in the source location'))
        return {}

    @api.depends('src_product_id')
    def _compute_store_convertible_products(self):
        lst = []
        if self.src_product_id:
            for prod in self.src_product_id.conversion_line:
                lst.append(prod.convertible_product.id)
                self.product_ids = [(6, 0, [i for i in lst])]

    def validate(self):
        if not self.conversion_line:
            raise UserError(_('Kindly Select Products to Convert'))
        inventory_loss = self.env['stock.location'].search([('usage', '=', 'inventory'), ('scrap_location', '=', False), ('return_location', '=', False)], limit=1)
        if not inventory_loss:
            raise UserError(_('Kindly map a conversion location'))
        allocte_qty = 0.0
        for line in self.conversion_line:
            if line.allocate_quantity == 0.0:
                raise UserError(_('Please enter the Allocation Quantity'))
            allocte_qty += line.allocate_quantity
        if allocte_qty != self.qty_to_convert:
            raise UserError(_('The given allocate Quantity must be equal to the Quantity given for conversion.'))
        vals_from = {
            'name': self.name + '/ SL',
            'product_id': self.src_product_id.id,
            'location_id': self.from_location.id,
            'location_dest_id': inventory_loss.id,
            'product_uom_qty': self.qty_to_convert,
            'product_uom': self.src_uom.id,
            'quantity_done': self.qty_to_convert,
            'state': 'confirmed',
            'move_line_ids': [(0, 0, {
                'product_id': self.src_product_id.id,
                'lot_id': self.src_lot.id or '',
                'product_uom_qty': 0,
                'product_uom_id': self.src_uom.id,
                'qty_done': self.qty_to_convert,
                'location_id': self.from_location.id,
                'location_dest_id': inventory_loss.id,
            })]
        }
        stock_move_from = self.env['stock.move'].create(vals_from)
        stock_move_from._action_done()
        for line in self.conversion_line:
            vals_to = {
                'name': self.name + '/ DL',
                'product_id': line.dest_product_id.id,
                'location_id': inventory_loss.id,
                'location_dest_id': line.to_location.id,
                'product_uom_qty': line.converted_qty,
                'product_uom': line.dest_uom.id,
                'quantity_done': line.converted_qty,
                'state': 'confirmed',
                'move_line_ids': [(0, 0, {
                    'product_id': line.dest_product_id.id,
                    'lot_id': line.dest_lot.id,
                    'product_uom_qty': 0,
                    'product_uom_id': line.dest_uom.id,
                    'qty_done': line.converted_qty,
                    'location_id': inventory_loss.id,
                    'location_dest_id': line.to_location.id,
                })]
            }
            stock_move_to = self.env['stock.move'].create(vals_to)
            stock_move_to._action_done()
        self.write({'state': 'done'})
        return True

    def cancel(self):
        self.write({'state': 'cancel'})
        return True

    def set_to_draft(self):
        self.write({'state': 'draft'})
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('product.conversion') or '/'
        res = super(ProductConversion, self).create(vals)
        return res

    def unlink(self):
        for conversion in self:
            if conversion.state == 'done':
                raise UserError(_('Warning! You cannot delete a validated Conversion'))
        return super(ProductConversion, self).unlink()


class ProductConversionLine(models.Model):
    _name = "product.conversion.line"
    _description = "Product Conversion Line"

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

    @api.onchange('dest_product_id')
    def onchange_product_uom(self):
        if not self.conversion_id.qty_to_convert:
            raise UserError(_('Kindly Enter the Quantity to Convert'))
        if self.dest_product_id:
            for ratio in self.conversion_id.src_product_id.conversion_line:
                if self.dest_product_id == ratio.convertible_product:
                    if not ratio.conversion_ratio:
                        raise UserError(_('There is no conversion Ratio for ' + str(self.dest_product_id.name)))
                    self.conversion_ratio = ratio.conversion_ratio
            self.dest_uom = self.dest_product_id.uom_id.id
        if not self.dest_product_id:
            self.dest_uom = False
            self.conversion_ratio = 0.0
        return {}

    @api.onchange('allocate_quantity')
    def onchange_allocate_qty(self):
        if not self.conversion_id.qty_to_convert:
            raise UserError(_('Kindly Enter the Quantity to Convert'))
        if self.allocate_quantity:
            self.converted_qty = self.conversion_ratio * self.allocate_quantity
        return {}


class ProductProduct(models.Model):
    _inherit = "product.product"

    conversion_line = fields.One2many('product.line', 'prod_id', string='Conversion')
    duplicate_product_check = fields.Boolean(string='Duplicate Product Check', compute="_compute_check_duplicate_convertible_product")

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