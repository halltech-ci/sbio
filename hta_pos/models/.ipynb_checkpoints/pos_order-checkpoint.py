# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HtaPos(models.Model):
    _inherit = 'pos.order'
    

    delivery_person = fields.Many2one(
        comodel_name="res.partner",
        string="Livreur",
    )

    date_delivery = fields.Datetime()


# class AssignPos(models.Model):
#     _name = 'assign.commands'
#     _description = "Assign Commande to Delivery Person"
#     _inherit = ["mail.thread", "mail.activity.mixin"]
#     _order = "id desc"

#     delivery_person = fields.Many2one(
#         comodel_name="res.partner",
#         string="Delivery Person",
#     )
#     purchase_lines = fields.Many2many(
#         comodel_name="pos.order",
#         string="Commands",
#         readonly=True,
#         copy=False,
#     )
#     date_delivery = fields.Datetime()


