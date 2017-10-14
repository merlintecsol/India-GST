# -*- coding: utf-8 -*-
# Part of openerp. See LICENSE file for full copyright and licensing details.

from openerp import api, models, fields, _


class WizardGstrB2B(models.TransientModel):
    _name = 'gstr.b2b'

    start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def print_b2b_report(self,vals):
        # invoice_obj = self.env['check.date']
        invoice_obj = self.env['check.date'].search([])
        if invoice_obj:
            invoice_obj[-1].write(
                            {'start_date':self.start_date,
                            'end_date':self.end_date,
                            })
        if not invoice_obj:
            invoice_obj.create(
                            {'start_date':self.start_date,
                            'end_date':self.end_date,
                            })

        return self.env["report"].get_action(self, 'account.gstr.b2b.xlsx')


class CheckDate(models.Model):
    _name = 'check.date'

    start_date = fields.Date('From Date',default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date',default=fields.Datetime.now(),required=True)
