# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import json

class barcode_product(models.Model):
    _inherit = 'stock.production.lot'
    

    date_create = fields.Datetime(string='Create Date', default=lambda self: fields.Datetime.now())
    time_expire = fields.Datetime(string='Date Expirate',default=lambda self: fields.Datetime.now()+timedelta(730))
    avail_locations = fields.Many2many('stock.location',string="Available locations",compute="_compute_avail_location")
    quant_text = fields.Text('Quant Qty',compute='_compute_avail_location')
    
    @api.depends('date_create')
    def _compute_exp_date(self):
        if self.date_create:
            date_create = self.date_create
            self.time_expire = datetime(date_create.year,date_create.month,date_create.day) + timedelta(730)

        
    @api.onchange('date_create','product_id.use_expiration_date','product_id.expiration_time')
    def onc_expirate_date_expire(self):
        if self.product_id.use_expiration_date:
            date_create = self.date_create
            self.time_expire = datetime(date_create.year,date_create.month,date_create.day) + timedelta(self.product_id.expiration_time) 
        else:
            date_create = self.date_create
            self.time_expire = datetime(date_create.year,date_create.month,date_create.day) + timedelta(730)
    
    
    @api.depends('quant_ids','quant_ids.location_id','quant_ids.quantity')
    def _compute_avail_location(self):
        for rec in self:
            if rec.quant_ids:
                rec.avail_locations = []
                locations = rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('location_id')
                rec.avail_locations = [(6,0,locations.ids)]
                rec.quant_text = ''
                aa = dict(zip((rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('location_id.id')),(rec.quant_ids.filtered(lambda x: x.quantity > 0 and x.location_id.usage == 'internal').mapped('quantity'))))
                rec.quant_text = json.dumps(aa)
            else:
#                 locations = rec.quant_ids.filtered(lambda x: x.location_id.usage == 'internal').mapped('location_id')
#                 rec.avail_locations = [(6,0,locations.ids)]
                rec.quant_text = ''
                aa = dict(zip(
                    (rec.quant_ids.filtered(lambda x: x.location_id.usage == 'internal').mapped('location_id.id'))
                    ))
                rec.quant_text = json.dumps(aa)

        
            