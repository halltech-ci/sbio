# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _
import json


class ProductLot(models.Model):
	_inherit = 'stock.production.lot'

	def _default_expiry_date(self):
		self.expiration_date.date() if self.expiration_date else False

	@api.onchange('expiration_date')
	def onc_expiration_date(self):
		self.expiry_date = self.expiration_date.date() if self.expiration_date else False

	@api.depends('name','product_id.barcode')
	def _compute_lot_name(self):
		for rec in self:
			rec.lot_name = ''
			if rec.barcode :
				rec.lot_name = str(rec.barcode) +'/'+ rec.name
			else:
				rec.lot_name = rec.name

	product_tmpl_id =fields.Many2one('product.template', string='Product Template',related ='product_id.product_tmpl_id')
	lot_name = fields.Char("Lot Name",compute="_compute_lot_name")
	barcode = fields.Char('Barcode',related ='product_id.barcode')
	expiration_date = fields.Datetime(string='Expiration Date')
	expiry_date =  fields.Date(string='Expiry Date', default=lambda self: self._default_expiry_date())
	product_qty = fields.Float('Quantity', compute='_product_qty',store=True)

	avail_locations = fields.Many2many('stock.location',string="Available locations",
		compute="_compute_avail_locations")
	quant_text = fields.Text('Quant Qty',compute='_compute_avail_locations')

	@api.depends('quant_ids','quant_ids.location_id','quant_ids.quantity')
	def _compute_avail_locations(self):
		for rec in self:
			rec.avail_locations = []
			locations = rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('location_id')
			rec.avail_locations = [(6,0,locations.ids)]
			rec.quant_text = ''
			aa = dict(zip(
				(rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('location_id.id')),
				(rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('quantity'))
				))
			rec.quant_text = json.dumps(aa)

class Product(models.Model):
	_inherit = "product.product"

	barcode_ids = fields.One2many('stock.production.lot','product_id',
		string='Barcodes Lots')


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	barcode_ids = fields.One2many(related='product_variant_ids.barcode_ids')


class pos_config(models.Model):
	_inherit = 'pos.config'

	show_stock_location = fields.Selection([('all', 'All Locations'),
		('specific', 'Operation Type Location')],default='all',string='Select Lots from')

	op_typ_loc_id = fields.Many2one('stock.location', string='Operation Type Location',
		related='picking_type_id.default_location_src_id')
