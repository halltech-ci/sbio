#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

from xml.dom import ValidationErr
from odoo.exceptions import ValidationError,UserError
from odoo import api, fields, models, api, _

import logging
_logger = logging.getLogger(__name__)

class StockQuant(models.Model):
	_inherit = 'stock.quant'

	@api.model
	def create(self, vals):
		if vals.get('product_id'):
			product = self.env['product.product'].sudo().browse(vals['product_id'])
			if product.is_pack:
				values = product._compute_quantities()
				# qty = values[product.product_tmpl_id.id]['qty_available']
				# outgoing_qty = values[product.product_tmpl_id.id]['outgoing_qty']
				# vals.update({
				# 	'inventory_quantity': qty,
				# })
		res = super(StockQuant, self).create(vals)
		return res

	def write(self, vals):
		self = self.sudo()
		for record in self:
			if record.product_id.is_pack:
				values = record.product_id._compute_quantities()
				# qty = values[record.product_id.product_tmpl_id.id]['qty_available']
				# outgoing_qty = values[record.product_id.product_tmpl_id.id]['outgoing_qty']
				# if vals.get('quantity') or vals.get('reserved_quantity') or vals.get('inventory_quantity'):
				# 	vals['inventory_quantity'] = qty
		return super(StockQuant, self).write(vals)



class ProductTemplate(models.Model):
	_inherit = 'product.template'


	@api.onchange('is_pack')
	def remove_variant(self):
		if self.attribute_line_ids:
			raise UserError('Please remove the variants from the product')
	
	@api.constrains('is_pack','wk_product_pack')
	def check_pack_lines(self):
		if self.is_pack:
			if not self.wk_product_pack:
				raise UserError(
                    'You can not create a pack without products!!!')

	def _compute_quantities_dict(self):
		res = super(ProductTemplate, self)._compute_quantities_dict()
		if len(self) > 1:
			pass
		else:
			variants_available = self.mapped('product_variant_ids')._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
			prod_available = res
			for template in self:
				qty_available = 0
				virtual_available = 0
				incoming_qty = 0
				outgoing_qty = 0
				for p in template.product_variant_ids:
					qty_available += variants_available[p.id]["qty_available"]
					virtual_available += variants_available[p.id]["virtual_available"]
					incoming_qty += variants_available[p.id]["incoming_qty"]
					outgoing_qty += variants_available[p.id]["outgoing_qty"]
					################################### CODE ADDED BY JAHANGIR ####################################
					if template.is_pack and template.wk_product_pack:

						if len(template.product_variant_ids) > 1:
							variants_list = template.product_variant_ids.ids
						else:
							variants_list = [template.product_variant_ids.id]
						for pp in template.wk_product_pack:
							variants_list.append(pp.product_id.id)
						
						variants = self.env['product.product'].browse(variants_list)
						variants_available.update(variants._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date')))
						qty_avail = []
						vir_avail = []
						inco_qty = []
						outgo_qty = []
						for pp in template.wk_product_pack:
							if pp.product_id and pp.product_quantity > 0 and pp.product_id.type not in ['consu','service']:
								qty_avail.append(variants_available[pp.product_id.id]["qty_available"]/pp.product_quantity)
								vir_avail.append(variants_available[pp.product_id.id]["virtual_available"]/pp.product_quantity)
								inco_qty.append(variants_available[pp.product_id.id]["incoming_qty"]/pp.product_quantity)
								outgo_qty.append(variants_available[pp.product_id.id]["outgoing_qty"]/pp.product_quantity)
						qty_available = qty_avail and min(qty_avail) or 0
						virtual_available = vir_avail and min(vir_avail) or 0
						incoming_qty = inco_qty and min(inco_qty) or 0
						outgoing_qty = inco_qty and min(outgo_qty) or 0
				################################### CODE CLOSED BY JAHANGIR ####################################
				prod_available[template.id].update({
					"qty_available": int(qty_available),
					"virtual_available": int(virtual_available),
					"incoming_qty": int(incoming_qty),
					"outgoing_qty": int(outgoing_qty),
				})

			return prod_available
		return res

class ProductProduct(models.Model):
	_inherit = 'product.product'

	def _compute_quantities(self):
		res = super(ProductProduct,self)._compute_quantities()
		for rec in self:
			if rec.is_pack:
				values = rec.product_tmpl_id._compute_quantities_dict()
				rec.qty_available = values[rec.product_tmpl_id.id]['qty_available']
				rec.virtual_available = values[rec.product_tmpl_id.id]['virtual_available']
		return res


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	def _get_delivered_qty(self):
		res = super(SaleOrderLine, self)._get_delivered_qty()
		if self.product_id.is_pack:
			return self.product_uom_qty
		return res

	@api.depends('product_id', 'customer_lead', 'product_uom_qty', 'product_uom', 'order_id.warehouse_id', 'order_id.commitment_date')
	def _compute_qty_at_date(self):
		res = super(SaleOrderLine,self)._compute_qty_at_date()

		for line in self:
			if line.product_id.is_pack:
				prod_available = line.product_id.product_tmpl_id._compute_quantities_dict()
				available_quantities = prod_available[line.product_id.product_tmpl_id.id]
				line.free_qty_today = available_quantities.get('qty_available',0)
				line.virtual_available_at_date = available_quantities.get('virtual_available',0)

		return res
