odoo.define('bi_pos_reprint_reorder.OrderPrintNoticeScreen', function (require) {
	'use strict';

	const ReceiptScreen = require('point_of_sale.ReceiptScreen');
	const Registries = require('point_of_sale.Registries');

	const OrderPrintNoticeScreen = (ReceiptScreen) => {
		class OrderPrintNoticeScreen extends ReceiptScreen {
			constructor() {
				super(...arguments);
			}
            back() {
				this.props.resolve({ confirmed: true, payload: null });
				this.trigger('close-temp-screen');
			}

		}
		OrderPrintNoticeScreen.template = 'OrderPrintNoticeScreen';
		return OrderPrintNoticeScreen;
	};

	Registries.Component.addByExtending(OrderPrintNoticeScreen, ReceiptScreen);

	return OrderPrintNoticeScreen;
});
