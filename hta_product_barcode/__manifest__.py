# -*- coding: utf-8 -*-
{
    'name': "hta_product_barcode",

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
    'category': 'Product Management',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['product',
                'stock',
                'stock_barcode',
                'barcodes',
               ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        
         # report barcode inherit 
#         'report_barcode/report_barcode_views.xml',
#         'report_barcode/report_simple_label_views.xml',
#         'report_barcode/with_price2x7_views.xml',
#         'report_barcode/with_price4x7_views.xml', 
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    #'post_init_hook': 'post_init_hook',
}
