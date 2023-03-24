odoo.define('bi_pos_reprint_reorder.POSOrdersScreen', function (require) {
	'use strict';

	const POSOrdersScreen = require('pos_orders_list.POSOrdersScreen');
	const Registries = require('point_of_sale.Registries');
	const {useState} = owl.hooks;
	const {useListener} = require('web.custom_hooks');

	const BiPOSOrdersScreen = (POSOrdersScreen) =>
		class extends POSOrdersScreen {
			constructor() {
				super(...arguments);
				useListener('click-reorder', this.clickReOrder);
				useListener('click-reprint', this.clickReprint);
                useListener('click-notice', this.clickNotice);
			}
			
			clickReOrder(event){
				let self = this;
				let order = event.detail;
				let o_id = parseInt(event.detail.id);
				let orderlines =  self.orderlines;				
				let pos_lines = [];

				for(let n=0; n < orderlines.length; n++){
					if (orderlines[n]['order_id'][0] ==o_id){
						pos_lines.push(orderlines[n])
					}
				}
				self.showPopup('ReOrderPopup', {
					'order': event.detail, 
					'orderlines':pos_lines,
				});
			}

			async clickReprint(event){
				let self = this;
				let order = event.detail;

				await self.rpc({
					model: 'pos.order',
					method: 'print_pos_receipt',
					args: [order.id],
				}).then(function(output) {
					let data = output;
					data['order'] = order;
					self.showTempScreen('OrderReprintScreen',data);
				});

			}
            
            async clickNotice(event){
				let self = this;
				let order = event.detail;

				await self.rpc({
					model: 'pos.order',
					method: 'print_pos_receipt',
					args: [order.id],
				}).then(function(output) {
					let data = output;
					data['order'] = order;
					self.showTempScreen('OrderNoticeScreen',data);
				});

			}
            
            async clickNoticeSelect(event){
				var products = this.pos.db.get_product_by_category(0);
                var list = [];
                for (var i = 0, len = products.length; i < len; i++) {
                    list.push({
                        'label': products[i].display_name,
                        'item': products[i],
                    });
                }

			}
		}
		
	Registries.Component.extend(POSOrdersScreen, BiPOSOrdersScreen);

	return POSOrdersScreen;
});


