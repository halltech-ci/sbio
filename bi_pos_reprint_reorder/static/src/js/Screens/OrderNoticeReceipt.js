odoo.define('bi_pos_reprint_reorder.OrderNoticeReceipt', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class OrderNoticeReceipt extends PosComponent {
		constructor() {
			super(...arguments);
		}
		
		get receiptBarcode(){
			let barcode = this.props.barcode;
			$("#barcode_print1").barcode(
				barcode, // Value barcode (dependent on the type of barcode)
				"code128" // type (string)
			);
		return true
		}
	}
	OrderNoticeReceipt.template = 'OrderNoticeReceipt';

	Registries.Component.add(OrderNoticeReceipt);

	return OrderNoticeReceipt;
});
