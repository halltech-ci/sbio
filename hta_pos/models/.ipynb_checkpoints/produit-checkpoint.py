
from odoo import models, fields, api

class ProduitTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    
    notice_fields = fields.Text()
    
class ProduitTemplateInherit(models.Model):
    _inherit = 'product.product'
    
    
    notice_fields = fields.Text()