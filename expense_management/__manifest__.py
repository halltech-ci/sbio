# -*- coding: utf-8 -*-
{
    'name': "expense_management",

    'summary': """
        Workflow for expense management""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Expenses',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'web_tour'],

    # always loaded
    'data': [
        'security/expense_management_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
