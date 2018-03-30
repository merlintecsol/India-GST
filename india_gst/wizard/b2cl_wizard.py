# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class WizardB2cl(models.TransientModel):
    _name = 'wizard.b2cl'

    start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def print_b2cl_report(self):
        data = {}
        data['form'] = self.read(['start_date','end_date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date','end_date'])[0])
        return self.env.ref('india_gst.gstr_b2cl_report').report_action(self, data=data)
