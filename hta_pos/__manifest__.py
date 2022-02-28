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
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale',
                'stock',
               
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
        
        #inherit report barcode
#         'report_barcode/report_simple_label_dymo_views.xml',
#         'report_barcode/report_simple_label4x7_views.xml',
#         'report_barcode/report_simple_label2x7_views.xml',
        
        # WIZARD
        'wizard/assign_commands.xml',
        'wizard/wizard_report_pos_views.xml',
        
        # Report
        'report/report_customer_list_by_product_views.xml',
        'report/report_pos_print_order_delivery.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
