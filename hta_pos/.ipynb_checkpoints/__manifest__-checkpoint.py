# -*- coding: utf-8 -*-
{
    'name': "hta_pos",

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
    'category': 'Sales/Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale',
                'stock',
                'report_xlsx',
                'crm',
                
                #'report_xlsx'
               ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payment_order.xml',
        'views/assign_commands_views.xml',
        'views/pos_order_views.xml',
        'views/stock_picking.xml',
        'views/produit_views.xml',
        'views/res_partner_views.xml',
        # 'views/pos_views_pivot.xml',
        # WIZARD
        'wizard/wizard_report_customer_sale_views.xml',
        'wizard/assign_commands.xml',
        'wizard/wizard_report_pos_views.xml',
        
        # Report
        'report/report_customer_list_by_product_views.xml',
        'report/report_pos_print_order_delivery.xml',
        
    ],
    'assets': {
        'web.assets_qweb': [
            'hta_pos/static/src/xml/pos_refund.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
