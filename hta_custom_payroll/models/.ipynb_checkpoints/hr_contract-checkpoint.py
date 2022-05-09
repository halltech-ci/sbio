# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContract(models.Model):
    _inherit = "hr.contract"
    
    prime_transport = fields.Monetary(string="Prime de Transport")
    indemnite_transport = fields.Monetary(string="Indemnité de Transport")
    indemnite_licencement = fields.Monetary(string="Indemnité de Licencement")
    indemnite_compensatrice = fields.Monetary(string="Indemnité de compensatrice préavis ")
    indemnite_conge = fields.Monetary(string="Indemnité de conge")
    prelevement_assurance_mci = fields.Monetary(string="Prélèvement Assurance Employé")
    pret = fields.Monetary(string="Prêt")
    prime_assurance_mci = fields.Monetary(string="Part Assurance Employeur")
    prime_communication = fields.Monetary(string="Communication")
    sursalaire = fields.Monetary(string="Sursalaire")
    prime_logement = fields.Monetary(string="Logement")
    prime_responsabilite = fields.Monetary(string="Responsabilité")
    prime_rendement = fields.Monetary(string="Prime de rendement")
    prime_salissure = fields.Monetary(string="Salissure")
    gratification = fields.Monetary(string="Gratification")
    autres_avantages = fields.Monetary(string="Autres Avantages")
    conges_payes = fields.Monetary(string="Congés Payés")
    salaire_brut = fields.Monetary(string="Salary Cost")
    salaire_base = fields.Monetary(string="Salary Base")
    avs = fields.Monetary(string="Avances et  Acomptes perçus")
    partner_id = fields.Many2one('res.partner', string="Partner")
    communication_flotte = fields.Monetary(string="Coût Communication Flotte")
    
    
    