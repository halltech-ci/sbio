from odoo import models, fields, api

class HtaPos(models.Model):
    _inherit = 'pos.order'
    

    customer_Phone = fields.Char()
    delivery_phone = fields.Char()
   

    @api.onchange("partner_id")
    def _onchange_customer_Phone(self):
        for rec in self:
            if rec.partner_id:
                rec.customer_Phone = rec.partner_id.phone
                
    @api.onchange("delivery_person")
    def _onchange_delivery_phone(self):
        for rec in self:
            if rec.delivery_person:
                rec.delivery_phone = rec.delivery_person.phone
                
                
                
                
                
class ProduitTemplateInherit(models.Model):
    _inherit = 'product.template'
    
    
    notice_fields = fields.Text()
    
class ProduitTemplateInherit(models.Model):
    _inherit = 'product.product'
    
    notice_fields = fields.Text()
    
    def get_product_multiline_notice_fields(self):
        """ Compute a multiline description of this product, in the context of sales
                (do not use for purchases or other display reasons that don't intend to use "description_sale").
            It will often be used as the default description of a sale order line referencing this product.
        """
        name = self.display_name
        if self.notice_fields:
            name += '\n' + self.notice_fields

        return name

