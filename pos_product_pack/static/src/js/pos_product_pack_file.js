/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('pos_product_pack.pos_product_pack', function(require) {
    "use strict";
    var models = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const ProductItem = require('point_of_sale.ProductItem');

    models.load_models([{
        model: 'product.product',
        condition: function(self) {
            return true; },
        fields: ['id', 'name', 'wk_product_pack', 'lst_price'],
        domain: function(self) {
            return [
                ['is_pack', '=', true]
            ]; },
        loaded: function(self, result) {
            self.set({ 'product_pack': result });
        },
    }, {
        model: 'product.pack',
        condition: function(self) {
            return true; },
        fields: ['id', 'product_id', 'product_quantity', 'uom_id', 'price', 'name'],
        domain: function(self) {
            return []; },
        loaded: function(self, result) {
            self.set({ 'wk_pack_product': result });
        },
    }], { 'after': 'product.product' });

    models.Orderline = models.Orderline.extend({
        getPackProduct: function(pack_product_id, product_price, product_qty) {
            self = this;
            var pack_product = self.pos.get('product_pack');
            var wk_pack_products = self.pos.get('wk_pack_product');
            var pack_product_list = [];
            var savedprice = 0;
            for (var i = 0; i < pack_product.length; i++) {
                if (pack_product[i].id == pack_product_id && (pack_product[i].wk_product_pack).length > 0) {
                    for (var j = 0; j < (pack_product[i].wk_product_pack).length; j++) {
                        for (var k = 0; k < wk_pack_products.length; k++) {
                            if (wk_pack_products[k].id == pack_product[i].wk_product_pack[j]) {
                                var product_val = { 'display_name': wk_pack_products[k].name, 'uom_id': wk_pack_products[k].uom_id, 'price': wk_pack_products[k].price };
                                pack_product_list.push({ 'product': product_val, 'qty': wk_pack_products[k].product_quantity * parseFloat(product_qty) });
                                savedprice += wk_pack_products[k].price * wk_pack_products[k].product_quantity * parseFloat(product_qty);
                            }
                        }
                    }
                    return { 'pack_product_list': pack_product_list, 'wk_pack_benefit': savedprice - product_price };
                }
            }
        },
        wk_get_unit: function(unit_id) {
            if (!unit_id) {
                return undefined;
            }
            return unit_id[1];
        },
    });

    models.Order = models.Order.extend({
        get_pack_product_benefits: function(orderlines) {
            var self = this;
            var savedprice = 0;
            var wk_quantity_price = 0
            var pack_products = self.pos.get('product_pack')
            var wk_pack_products = self.pos.get('wk_pack_product')
            _.each(orderlines, function(orderline) {
                _.each(pack_products, function(pack_product) {
                    if (orderline.product.id == pack_product.id) {
                        _.each(pack_product.wk_product_pack, function(pack_product_ids) {
                            for (var k = 0; k < wk_pack_products.length; k++) {
                                if (wk_pack_products[k].id == pack_product_ids) {
                                    savedprice = savedprice + (wk_pack_products[k].price * wk_pack_products[k].product_quantity * orderline.quantity);
                                }
                            }
                        });
                        wk_quantity_price += orderline.quantity * orderline.product.lst_price;
                    }
                });
            });
            savedprice -= wk_quantity_price;
            if (savedprice > parseFloat(0))
                return savedprice;
            return 0;
        },
    });

    // Inherit Orderline----------------
    const PosResProductItem = (ProductItem) =>
		class extends ProductItem {
            wk_is_pack_product(product_id) {
                var self = this;
                var pack_product = self.env.pos.get('product_pack');
                for (var i = 0; i < pack_product.length; i++) {
                    if (pack_product[i].id == product_id) {
                        return true;
                    }
                }
            }     
		};
    Registries.Component.extend(ProductItem, PosResProductItem);  
});
