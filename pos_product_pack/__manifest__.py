# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "POS Product Pack",
  "summary"              :  """The module allows you to combine various different products into a product bundle and sell it as a single unit in the Odoo POS.""",
  "category"             :  "Point of Sale",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-POS-Product-Pack.html",
  "description"          :  """Odoo POS Product Pack
Odoo POS product packaging
Odoo product pack
product package in Odoo
POS make bundled products
bundled products marketplace
Odoo marketplace Product packages
create Product bundles Odoo
Marketplace Product bundles
Manage Packages
Product Package
Wholesale Product
Wholesale Management""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pos_product_pack&custom_url=/pos/auto",
  "depends"              :  [
                             'point_of_sale',
                             'wk_product_pack',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/pos_product_pack.xml',
                            ],
  "demo"                 :  ['data/pos_product_pack_demo.xml'],
  #"qweb"                 :  ['static/src/xml/pos_product_pack.xml'],
  "assets"               :  {
                                'point_of_sale.assets': [
                                  "pos_product_pack/static/src/js/pos_product_pack_file.js",
                                  "pos_product_pack/static/src/css/pos_product_pack.css",
                                  ],
                                  'web.assets_qweb': [
                                    'pos_product_pack/static/src/xml/pos_product_pack.xml',
                                ],
                              },
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  27,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
}
