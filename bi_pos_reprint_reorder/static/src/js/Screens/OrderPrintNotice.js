odoo.define('bi_pos_reprint_reorder.OrderPrintNotice', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');

	class OrderPrintNotice extends PosComponent {
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
	OrderPrintNotice.template = 'OrderPrintNotice';

	Registries.Component.add(OrderPrintNotice);

	return OrderPrintNotice;
});
