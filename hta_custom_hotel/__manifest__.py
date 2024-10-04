# -*- coding: utf-8 -*-
{
    'name': "hta_custom_hotel",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Hotel Restaurant',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hotel_reservation', "hotel",],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        "wizard/reservation_register_payment_wizard.xml",
        "views/hotel_reservation_views.xml",
        "views/hotel_folio_views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "license": "LGPL-3",
}
