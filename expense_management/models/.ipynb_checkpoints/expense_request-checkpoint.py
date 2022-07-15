# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ExpenseRequest(models.Model):
    _name "expense.request"
    _description = "Manage expense request workflow"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    