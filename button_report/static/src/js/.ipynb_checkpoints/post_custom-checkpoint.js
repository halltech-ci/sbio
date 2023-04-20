odoo.define('button_report.ReportTicket', function(require) {
	'use strict';

	const PosComponent = require('point_of_sale.PosComponent');
	const ProductScreen = require('point_of_sale.ProductScreen');
	const { useListener } = require('web.custom_hooks');
	const Registries = require('point_of_sale.Registries');

	class ReportTicket extends PosComponent {
		constructor() {
			super(...arguments);
			useListener('click', this.onClick);
		}
        async onClick() {
            console.log('Yooo la rue ')
        }
        
        	}

        
        ReportTicket.template = 'ReportTicket';

	ProductScreen.addControlButton({
		component: ReportTicket,
		condition: function() {
			return this.env.pos.config.allow_partical_payment;
		},
	});

	Registries.Component.add(ReportTicket);

	return ReportTicket;

    });