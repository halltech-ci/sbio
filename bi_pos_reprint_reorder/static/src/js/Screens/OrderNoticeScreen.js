odoo.define('bi_pos_reprint_reorder.OrderNoticeScreen', function (require) {
	'use strict';

	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
	const Registries = require('point_of_sale.Registries');

	const OrderNoticeScreen = (ReceiptScreen) => {
		class OrderNoticeScreen extends ReceiptScreen {
			constructor() {
				super(...arguments);
			}

			back() {
				this.props.resolve({ confirmed: true, payload: null });
				this.trigger('close-temp-screen');
			}
		}
		OrderNoticeScreen.template = 'OrderNoticeScreen';
		return OrderNoticeScreen;
	};

	Registries.Component.addByExtending(OrderNoticeScreen, ReceiptScreen);

	return OrderNoticeScreen;
});
