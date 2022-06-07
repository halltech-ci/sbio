# -*- coding: utf-8 -*-
{
    'name': "expense_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Depenses',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
               'project',
               'account'],

    # always loaded
    'data': [
        'security/expense_management_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #Menu
        'views/res_config_settings_views.xml',
        'views/expense_management_menu.xml',
        #views
        'views/account_bank_statement_views.xml',
        'views/product_template_views.xml',
        'views/expense_line_reconcile_views.xml',
        'views/bank_statement_line_reconcile_view.xml',
        #data
        'data/mail_template.xml',
        'data/expense_request_seq.xml',
        'data/assets_backend.xml',
        
    ],
    'qweb':[
      'static/src/xml/expense_reconciliation.xml',  
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
