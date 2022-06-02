

# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round
import time

class ProductConversion(models.Model):
    _name = "product.reconversion"
    _description = "Model for reproduction product mrp"
    
    name = fields.Text(string="Name", default='/')
    state = fields.Selection([('draft', 'Draft'), ('reserve', 'reserved'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft')
    src_product_id = fields.Many2one('product.product', string='Product')
    src_uom = fields.Many2one('uom.uom', string="Unit of measure", related="src_product_id.uom_id")
    src_lot = fields.Many2one('stock.production.lot', string='Source Lot')
    src_product_tracking = fields.Selection(related='src_product_id.tracking', readonly=True)
    from_location = fields.Many2one('stock.location', string='Source Location')
    stock_qty = fields.Float(string="Stock Quantity", digits='Product Price',)
    #qty_done = fields.Float(string="Quantity Done", digits='Product Price', compute='_compute_qty_done')
    add_qty = fields.Float(string="Add Quantity", digits='Product Price')
    #qty_lost = fields.Float(string="Lost Quantity", digits='Product Price')
    reconversion_line = fields.One2many('product.reconversion.line', 'reconversion_id', string='Reconversion Line')
    product_ids = fields.Many2many('product.product', string='product ids', compute="_compute_store_convertible_products", store=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('product.conversion'))
    date = fields.Date(string='Date', index=True, default=time.strftime('%Y-%m-%d'))
    
    def _check_availlable_qty(self):
        qty = 0
        
    def _get_default_qty_to_convert(self):
        qty = 0
        
    @api.onchange('src_product_id')
    def _onchange_src_product_id(self):
        if self.src_product_id:
            if self.src_product_tracking != 'lot':
                raise ValidationError(_('Le suivi par lot n\'est pas activé pour cet article'))
    
    @api.onchange('src_lot')
    def _onchange_src_lot(self):
        for rec in self:
            if rec.src_product_id and rec.from_location:
                rec.qty_to_convert = rec.src_lot.product_qty
    
    """                
    def _get_default_qt_to_convert(self):
        for prod in self:
            if prod.src_product_id.src_product_tracking == 'lot':
                prod.qty_to_convert = prod.src_lot.product_qty
            else:
              raise ValidationError(_('Le suivi par lot n\'est pas activé pour cet article'))
    """                                  
                                      
    @api.onchange('conversion_line')
    def _onchange_qty_used(self):
        for prod in self:
            qty_done = 0
            if len(prod.conversion_line.ids) > 0:
                for line in prod.conversion_line:
                    qty_done += line.allocate_quantity
                self.qty_used = qty_done
                
    @api.onchange('qty_used')
    def _onchange_qty_lost(self):
        for prod in self:
            qty_lost = 0
            if len(prod.conversion_line.ids) > 0:
                for line in prod.conversion_line:
                    qty_lost += line.conversion_ratio * line.qty_done
                self.qty_lost = qty_lost - self.qty_used
    
    @api.onchange('conversion_line')
    def _onchange_qty_lost(self):
        for prod in self:
            qty_lost = 0
            if len(prod.conversion_line.ids) > 0:
                for line in prod.conversion_line:
                    qty_lost += line.conversion_ratio * line.qty_done
                self.qty_lost = qty_lost - self.qty_used
                
    @api.constrains('qty_to_convert')
    def _check_qty_to_convert(self):
        for rec in self:
            if rec.src_lot.product_qty < rec.qty_to_convert:
                raise ValidationError(_('La quantité à convertir est supérieure à la quantité disponible en stock pour ce lot'))
            
    
    @api.depends('src_product_id')
    def _compute_store_convertible_products(self):
        lst = []
        if self.src_product_id:
            lst = self.env["product.line"].search([('prod_id', '=', self.src_product_id.id)]).mapped('convertible_product')
            self.product_ids = lst
        
    
    def reserve_qty(self):
        #self._compute_allocate_qty()
        if not self.conversion_line:
            raise UserError(_('Veuillez choisir les articles'))
        inventory_loss = self.env['stock.location'].search([('usage', '=', 'inventory'), ('scrap_location', '=', False), ('return_location', '=', False)], limit=1)
        if not inventory_loss:
            raise UserError(_('Kindly map a conversion location'))
        allocte_qty = 0.0
        for line in self.conversion_line:
            if line.allocate_quantity == 0.0:
                raise UserError(_('Veuillez indiquer la quantité à convertir'))
            allocte_qty += line.allocate_quantity
        if allocte_qty > self.qty_to_convert:
            raise UserError(_('Quantité allouée supérieure à la quantité disponible.'))
        self.write({'state': 'reserve'})
    
    
    def validate(self):
        self._compute_allocate_qty()
        if not self.conversion_line:
            raise UserError(_('Veuillez choisir les articles'))
        inventory_loss = self.env['stock.location'].search([('usage', '=', 'inventory'), ('scrap_location', '=', False), ('return_location', '=', False)], limit=1)
        if not inventory_loss:
            raise UserError(_('Kindly map a conversion location'))
        allocte_qty = 0.0
        for line in self.conversion_line:
            if line.allocate_quantity == 0.0:
                raise UserError(_('Veuillez indiquer la quantité à convertir'))
            allocte_qty += line.allocate_quantity
        if allocte_qty > self.qty_to_convert:
            raise UserError(_('Quantité allouée supérieure à la quantité disponible.'))
        vals_from = {
            'name': self.name + '/ SL',
            'product_id': self.src_product_id.id,
            'location_id': self.from_location.id,
            'location_dest_id': inventory_loss.id,
            'product_uom_qty': self.qty_to_convert,
            'product_uom': self.src_uom.id,
            'quantity_done': self.qty_used,
            'state': 'confirmed',
            'move_line_ids': [(0, 0, {
                'product_id': self.src_product_id.id,
                'lot_id': self.src_lot.id or '',
                'product_uom_qty': 0,
                'product_uom_id': self.src_uom.id,
                'qty_done': self.qty_used,
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
                'quantity_done': line.qty_done,
                'state': 'confirmed',
                'move_line_ids': [(0, 0, {
                    'product_id': line.dest_product_id.id,
                    'lot_id': line.dest_lot.id,
                    'product_uom_qty': 0,
                    'product_uom_id': line.dest_uom.id,
                    'qty_done': line.qty_done,
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
        #self._compute_allocate_qty()
        return res

    def unlink(self):
        for conversion in self:
            if conversion.state == 'done':
                raise UserError(_('Warning! You cannot delete a validated Conversion'))
        return super(ProductConversion, self).unlink()
    
    #@api.depends('conversion_line')
    def _compute_allocate_qty(self):
        for line in self.conversion_line:
            if line.dest_product_id:
                prefixe = line.dest_product_id.default_code or ""
                quantity = str(int(line.qty_done))
                lot = line.conversion_id.src_lot.name
                new_lot = "{0}{1}{2}{3}{4}".format(prefixe, quantity, lot,str(int(line.conversion_ratio)), 'k')
                dest_lot = self.env['stock.production.lot'].create({
                    'name': new_lot,
                    'product_id': line.dest_product_id.id,
                    'product_qty': line.qty_done,
                    'company_id': line.conversion_id.company_id.id,
                }
                )
                line.dest_lot = dest_lot
    
class ProductConversionLinem(models.Model):
    _name = "product.reconversion.line"
    _description = "Line for product reconversion"
    
    reconversion_id = fields.Many2one('product.reconversion', string='Reconversion id')
    conversion_ratio = fields.Float(string='Conversion Ratio',)
    dest_product_id = fields.Many2one('product.product', string="Product")
    dest_uom = fields.Many2one('uom.uom', string="Unit of measure", related="dest_product_id.uom_id")
    dest_lot = fields.Many2one('stock.production.lot', string='Destination Lot',)
    to_location = fields.Many2one('stock.location', string='Destination Location')
    converted_qty = fields.Float(string='Converted Qty')
    dest_product_tracking = fields.Selection(related='dest_product_id.tracking', readonly=True)
    allocate_quantity = fields.Float(string='Allocate Qty', digits='Product Price')
    company_id = fields.Many2one(related='conversion_id.company_id', string='Company', store=True, readonly=True)
    qty_done = fields.Integer(string='Qty Done',)
    
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
                
    
        
    """
    @api.onchange('dest_product_id')
    def _onchange_dest_product_id(self):
        for line in self:
            if line.dest_product_id:
                if line.dest_product_id.tracking == 'lot':
                    line.dest_lot = line.conversion_id.src_lot.id
                else:
                    raise UserError(_('Veuillez activer le suivi par lot sur l\'article:' + str(line.dest_product_id.name)))
    """
