# -*- coding: utf-8 -*-
{
    'name': "hta_sale_ssbio",

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
    'category': 'Sales/Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sales_team','sale_management',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'security/sale_order_security.xml',
        'security/stock_security.xml',
        'views/views.xml',
        'views/templates.xml',
        
        #views
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
