# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _

class WizardB2b(models.TransientModel):
    _name = 'wizard.b2b'

    start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def print_b2b_report(self):
        data = {}
        data['form'] = self.read(['start_date','end_date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date','end_date'])[0])
        # b2b = self.env['report.gst.b2b'].generate_xlsx_report(self, 'gst.b2b',data=data)
        # return b2b
        # xls_report= GstrB2BXlsx.generate_xlsx_report(self, 'gst.b2b.xls',data=data)
        # return self.env['report.gst.b2b'].generate_xlsx_report(self,'report.gst.b2b', data=data)
        return self.env.ref('india_gst.gstr_b2b_report').report_action(self, data=data)

        # return self.env['report'].get_action(self,'report.gst.b2b', data=data)
