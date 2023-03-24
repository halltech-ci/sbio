# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.http import request

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)],'sale': [('readonly', False)]}, copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
     
#     state = fields.Selection(selection_add=[
#         ('waiting_for_approval', 'Attente de validation'),
#         ('approve', 'Approuve'),
#         ('sent',),
#         ]
#     )
# #     approver_id = fields.Many2one('res.users', string="Approver")
    
#     def ask_for_approval(self):
#         for rec in self:
#             if not rec.approver_id:
#                 raise UserError(_('You must choose approver before.'))
#             self.send_mail_to_approver()
#             rec.state = 'waiting_for_approval'
            
    
#     def action_approve(self):
#         for rec in self:
#             rec.state = 'approve'
    
#     def action_quotation_send(self):
#         res = super(SaleOrder,self).action_quotation_send()
#         if res:
#             for rec in self:
#                 rec.state = 'sent'
#         return res
    
#     def send_mail_to_approver(self):
#         #self.ensure_one()
#         subject = 'Approval request'
#         recipients = self.approver_id.email
#         base_url = request.env['ir.config_parameter'].get_param('web.base.url')
#         base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
#         message = "<p>Dear {0}</p>".format(self.approver_id.name) + "<p>You have approval request for quotation {0}</p>".format(self.name) + "<p>Click the bellow link to approve</p>"
#         message_body = message + base_url
#         template_obj = self.env['mail.mail']
#         template_data = {
#             'subject': subject,
#             'body_html': message_body,
#             'email_to': recipients
#         }
#         template_id = template_obj.create(template_data)
#         template_obj.send(template_id)
#         template_id.send()
#         #mail_template = self.env.ref('hta_sale_approval.email_template_sale_approval_mail')
#         #mail_template.send_mail(self.id,force_send=True)
#         return True
    
    