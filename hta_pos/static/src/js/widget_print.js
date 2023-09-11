odoo.define('hta_pos.print_report', function (require) {
    'use strict';

    var core = require('web.core');
    var FormController = require('web.FormController');

    var PrintReportControllerMixin = {
        renderButtons: function ($node) {
            this._super.apply(this, arguments);

            if (this.$buttons) {
                var self = this;
                this.$buttons.on('click', '.btn-primary', function () {
                    self.printReport();
                });
            }
        },

        printReport: function () {
            var self = this;
            var reportUrl = '/web/report/html/mon_module.report_ticket_notice';

            var params = {
                model: 'report.notice.wizard',
                id: self.model.get(self.handle, {raw: true}).res_id,
                report_type: 'qweb-pdf',
                context: self.getSession().user_context,
            };

            core.bus.trigger('do-action', {
                action_data: {
                    type: 'ir.actions.report',
                    report_type: 'qweb-pdf',
                    report_name: 'mon_module.report_ticket_notice',
                    report_file: 'mon_module.report_ticket_notice',
                    data: params,
                },
                download: true,
            });
        },
    };

    FormController.include(PrintReportControllerMixin);

    return PrintReportControllerMixin;
});
