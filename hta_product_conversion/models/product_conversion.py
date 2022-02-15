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
    src_uom = fields.Many2one('uom.uom', string="Unit of measure", related="src_product_id.uom_id")
    src_lot = fields.Many2one('stock.production.lot', string='Source Lot')
    src_product_tracking = fields.Selection(related='src_product_id.tracking', readonly=True)
    from_location = fields.Many2one('stock.location', string='Source Location')
    qty_to_convert = fields.Float(string="Quantity To Convert", digits='Product Price')
    qty_done = fields.Float(string="Quantity Done", digits='Product Price', compute='_compute_qty_done')
    conversion_line = fields.One2many('product.conversion.line', 'conversion_id', string='Conversion Line')
    product_ids = fields.Many2many('product.product', string='product ids', compute="_compute_store_convertible_products", store=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.conversion'))
    date = fields.Date(string='Date', index=True, default=time.strftime('%Y-%m-%d'))
    
    def _check_availlable_qty(self):
        qty = 0
        
    def _get_default_qty_to_convert(self):
        qty = 0
        
        
        
    
    def _compute_qty_done(self):
        for prod in self:
            qty_done = 0
            if len(prod.conversion_line.ids) > 0:
                for line in prod.conversion_line:
                    qty_done += line.converted_qty * line.conversion_ratio
                self.qty_done = qty_done
    
    
    @api.depends('src_product_id')
    def _compute_store_convertible_products(self):
        lst = []
        if self.src_product_id:
            lst = self.env["product.line"].search([('prod_id', '=', self.src_product_id.id)]).mapped('convertible_product')
            self.product_ids = lst
        
    
    def validate(self):
        if not self.conversion_line:
            raise UserError(_('Veuillez choisir les produits'))
        inventory_loss = self.env['stock.location'].search([('usage', '=', 'inventory'), ('scrap_location', '=', False), ('return_location', '=', False)], limit=1)
        if not inventory_loss:
            raise UserError(_('Kindly map a conversion location'))
        allocte_qty = 0.0
        for line in self.conversion_line:
            if line.allocate_quantity == 0.0:
                raise UserError(_('Veuillez indiquer la quantité à allouer'))
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
    
class ProductConversionLinem(models.Model):
    _name = "product.conversion.line"
    _description = "Line for product conversion"
    
    conversion_id = fields.Many2one('product.conversion', string='Conversion id')
    conversion_ratio = fields.Float(string='Conversion Ratio', compute='_get_conversion_ration')
    dest_product_id = fields.Many2one('product.product', string="Product")
    dest_uom = fields.Many2one('uom.uom', string="Unit of measure", related="dest_product_id.uom_id")
    dest_lot = fields.Many2one('stock.production.lot', string='Destination Lot')
    to_location = fields.Many2one('stock.location', string='Destination Location')
    converted_qty = fields.Float(string='Converted Quantity')
    dest_product_tracking = fields.Selection(related='dest_product_id.tracking', readonly=True)
    allocate_quantity = fields.Float(string='Allocate Quantity', digits='Product Price')
    company_id = fields.Many2one(related='conversion_id.company_id', string='Company', store=True, readonly=True)
    
    @api.depends('conversion_id.src_product_id')
    def _get_conversion_ration(self):
        for line in self:
            line.conversion_ratio = self.env['product.line'].search([('convertible_product', "=", line.dest_product_id.id), ('prod_id', '=', self.conversion_id.src_product_id.id)]).conversion_ratio
            
    @api.onchange('dest_product_id')
    @api.depends('conversion_id.src_product_id')
    def _onchange_product_id(self):
        for line in self:
            line.conversion_ratio = self.env['product.line'].search([('convertible_product', "=", line.dest_product_id.id), ('prod_id', '=', self.conversion_id.src_product_id.id)]).conversion_ratio
            
    @api.onchange('allocate_quantity')
    @api.depends('conversion_ratio')
    def _onchange_allocate_quantity(self):
        for line in self:
            if line.conversion_ratio != 0:
                line.converted_qty = int(line.allocate_quantity / line.conversion_ratio)
        
        
    
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
    
    
