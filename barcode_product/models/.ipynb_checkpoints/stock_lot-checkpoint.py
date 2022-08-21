# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import json

class barcode_product(models.Model):
    _inherit = 'stock.production.lot'
    

    date_create = fields.Datetime(string='Create Date', default=lambda self: fields.Datetime.now())
    time_expire = fields.Datetime(string='Date Expirate',default=lambda self: fields.Datetime.now()+timedelta(730))
    
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

        
            