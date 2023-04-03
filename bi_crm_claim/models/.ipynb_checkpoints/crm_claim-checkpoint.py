# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class crm_claim_stage(models.Model):
    _name = "crm.claim.stage"
    _description = "Claim stages"
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Used to order stages. Lower is better.",default=lambda *args: 1)
    team_ids = fields.Many2many('crm.team', 'crm_team_claim_stage_rel', 'stage_id', 'team_id', string='Teams',
                        help="Link between stages and sales teams. When set, this limitate the current stage to the selected sales teams.")
    case_default = fields.Boolean('Common to All Teams',
                        help="If you check this field, this stage will be proposed by default on each sales team. It will not assign this stage to existing teams.")

    _defaults = {
        'sequence': lambda *args: 1
    }                        
    

class crm_claim(models.Model):
    _name = "crm.claim"
    _description = "Claim"
    _order = "priority,date desc"
    _inherit = ['mail.thread']

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        team_id = self.env['crm.team'].sudo()._get_default_team_id()
        return self._stage_find(team_id=team_id.id, domain=[('sequence', '=', '1')])

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    id = fields.Integer('ID', readonly=True)
    name = fields.Char('Objet de la réclamation', required=True)
    active = fields.Boolean('Active',default=lambda *a: 1)
    action_next = fields.Char('Prochaine action')
    date_action_next = fields.Datetime('Date de la prochaine action')
    description = fields.Text('Description')
    resolution = fields.Text('Resolution')
    create_date = fields.Datetime('Date de création' , readonly=True)
    write_date = fields.Datetime('Date de mise à jour' , readonly=True)
    date_deadline = fields.Datetime('Date limite')
    date_closed = fields.Datetime('Fermé', readonly=True)
    date = fields.Datetime('Date de réclamation', default=lambda self: self._context.get('date', fields.Datetime.now()))
    categ_id = fields.Many2one('crm.claim.category', 'Categorie')
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority',default='1')
    type_action = fields.Selection([('correction','Action corrective'),('prevention','Action préventive')], 'Type action')
    user_id = fields.Many2one('res.users', 'Responsable', default=_default_user)
    user_fault = fields.Char('Responsable des troubles')
    team_id = fields.Many2one('crm.team', 'Équipe de vente',
                        help="Responsible sales team."\
                                " Define Responsible user and Email account for"\
                                " mail gateway.")
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env['res.company']._company_default_get('crm.case'))
    partner_id = fields.Many2one('res.partner', 'Client(e)')
    email_cc = fields.Text('Watchers Emails', help="These email addresses will be added to the CC field of all inbound and outbound emails for this record before being sent. Separate multiple email addresses with a comma")
    email_from = fields.Char('Email', help="Destination email for email gateway.",related='partner_id.email')
    partner_phone = fields.Char('Téléphone', related='partner_id.phone')
    stage_id = fields.Many2one ('crm.claim.stage', 'Stage',
                domain="['|', ('team_ids', '=', team_id), ('case_default', '=', True)]")    
    cause = fields.Text('Root Cause',help="Après analyse, la cause profonde du problème posé")
    product_ids = fields.Many2many('product.product', string="Produits achetés",domain="[('sale_ok', '=', True)]")
    
    
    
    @api.depends('partner_id')
    def _compute_product_ids(self):
        for claim in self:
            if claim.partner_id:
                lines = self.env['pos.order'].search([
                    ('partner_id', '=', claim.partner_id.id),
                    ('state', 'in', ['done','paid','invoiced']),
                ]).mapped('lines')
                product_ids = lines.mapped('product_id')
                claim.product_ids = product_ids
            else:
                claim.product_ids = False

    @api.onchange('partner_id')
    def onchange_product_ids(self):
        if self.partner_id:
            orders = self.env['pos.order'].search([('partner_id', '=', self.partner_id.id),('state', 'in', ['done','paid','invoiced'])])
            product_ids = []
            for order in orders:
                product_ids += order.lines.filtered(lambda l: l.product_id).mapped('product_id').ids
            self.product_ids = [(6, 0, product_ids)]
        else:
            self.product_ids = False
        # for claim in self:
        #     if claim.partner_id:
        #         lines = self.env['pos.order'].search([
        #             ('partner_id', '=', claim.partner_id.id),
        #             ('state', 'in', ['done','paid','invoiced']),
        #         ]).mapped('lines')
        #         product_ids = lines.mapped('product_id')
        #         claim.product_ids = [(6, 0, product_ids.ids)]
        #     else:
        #         claim.product_ids = False
        

    @api.onchange('partner_id')
    def onchange_partner_id(self, email=False):
        if not self.partner_id:
            return {'value': {'email_from': False, 'partner_phone': False}}
        address = self.pool.get('res.partner').browse(self.partner_id)
        return {'value': {'email_from': self.partner_id.email, 'partner_phone': self.partner_id.phone}}

    @api.model
    def create(self, vals):
        context = dict(self._context or {})
        if vals.get('team_id') and not self._context.get('default_team_id'):
            context['default_team_id'] = vals.get('team_id')

        # context: no_log, because subtype already handle this
        return super(crm_claim, self).create(vals)

    def message_new(self,msg, custom_values=None):
        if custom_values is None:
            custom_values = {}
        desc = html2plaintext(msg.get('body')) if msg.get('body') else ''
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'description': desc,
            'email_from': msg.get('from'),
            'email_cc': msg.get('cc'),
            'partner_id': msg.get('author_id', False),
        }
        if msg.get('priority'):
            defaults['priority'] = msg.get('priority')
        defaults.update(custom_values)
        return super(crm_claim, self).message_new(msg, custom_values=defaults)

class res_partner(models.Model):
    _inherit = 'res.partner'

    def _claim_count(self):
        for claim in self:
            claim_ids = self.env['crm.claim'].search([('partner_id','=',claim.id)])
            claim.claim_count = len(claim_ids)

    def claim_button(self):
        self.ensure_one()
        return {
            'name': 'Partner Claim',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'crm.claim',
            'domain': [('partner_id', '=', self.id)],
        }
        
    claim_count = fields.Integer(string='# Claims',compute='_claim_count')

class crm_claim_category(models.Model):
    _name = "crm.claim.category"
    _description = "Category of claim"

    name = fields.Char('Name', required=True, translate=True)
    team_id = fields.Many2one('crm.team', 'Sales Team')
