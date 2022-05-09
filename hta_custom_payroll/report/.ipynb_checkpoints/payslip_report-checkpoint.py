# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from datetime import date, datetime

class FichePayeParser(models.AbstractModel):
    _name = 'report.hta_custom_hr.report_hta_payslip_template'
    _description = "Payslip report"

    def get_payslip_lines(self, objs):
        res = []
        ids = []
        for item in objs:
            if item.appears_on_payslip is True and not item.salary_rule_id.parent_rule_id:
                ids.append(item.id)
        if ids:
            res = self.env['hr.payslip.line'].browse(ids)
        return res

    def get_total_by_rule_category(self, obj, code):
        category_total = 0
        category_id = self.env['hr.salary.rule.category'].search([('code', '=', code)], limit=1).id
        if category_id:
            line_ids = self.env['hr.payslip.line'].search([('slip_id', '=', obj.id), ('category_id', 'child_of', category_id)])
            for line in line_ids:
                category_total += line.total
        return category_total
    
    #Here obj represent payslip object
    def parse_payslip_lines(self, obj):
        code_dict = {}
        p_lines = self.env['hr.payslip'].search([('id', '=', obj.id)]).line_ids
        code_dict = {}
        for line in p_lines:
            code = line.code
            name = line.name
            val = line.amount
            dico = {code:[name, val],}#example: TH:['Taux Horaire', 177.33]
            code_dict.update(dico)
        return code_dict
        
    def get_employer_line(self, obj, parent_line):
        return self.env['hr.payslip.line'].search([('slip_id', '=', obj.id), ('salary_rule_id.parent_rule_id.id', '=', parent_line.salary_rule_id.id)], limit=1)

    @api.model
    def _get_report_values(self, docids, data=None):

        payslip = self.env['hr.payslip'].browse(docids)
        employee = payslip.employee_id.id
        first = datetime(datetime.today().year, 1, 1)
        last = datetime(datetime.today().year, 12, 31)
       
        annee = first.year
        domaine = [
            ('employee_id', '=', employee),
            ('date_start', '>=', first),
            ('date_stop', '<=', last)
                ]
        work_entries = self.env['hr.work.entry'].search(domaine)
        duration = 0
        for work_entry in work_entries:
            duration += work_entry.duration
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'data': data,
            'docs': payslip,
            'lang': "fr_FR",
            'get_payslip_lines': self.get_payslip_lines,
            'get_total_by_rule_category': self.get_total_by_rule_category,
            'get_employer_line': self.get_employer_line,
            'parse_payslip_lines': self.parse_payslip_lines,
            'duration':duration,
            'annee':annee
        }
