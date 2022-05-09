# -*- coding: utf-8 -*-
{
    'name': "hta_custom_payroll",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Payroll',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr',
                'hr_payroll',
                'account'
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_salary_rule_views.xml',
        #Data
        'data/payroll_data.xml',
        #Report
        'report/payslip_report.xml',
        'report/payslip_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
