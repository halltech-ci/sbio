odoo.define('pos_delete_orderline.Report_tickets', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { useState } = owl.hooks;
    const rpc = require('web.rpc');

    class Report_tickets extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            const pos = this.env.pos;
            const wizard_id = await rpc.query({
                model: 'create.report.wizard',
                method: 'create',
                args: [{listProduct: []}],
            
            });
            await pos.do_action({
                type: 'ir.actions.act_window',
                res_model: 'create.report.wizard',
                res_id: wizard_id,
                views: [[false, 'form']],
                target: 'new',
            });
        }
    }

    Report_tickets.template = 'Report_tickets';

    ProductScreen.addControlButton({
        component: Report_tickets,
        condition: function() {
            return this.env.pos;
        },
    });

    Registries.Component.add(Report_tickets);

    return Report_tickets;
});
