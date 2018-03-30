from odoo import models
import datetime

class GstrB2BXlsx(models.AbstractModel):
    _name = 'report.gst.b2b'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('B2B')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        y = 'Yes'
        n = 'No'


        worksheet.write('A%s' %(row), 'GSTIN/UIN of Recipient')
        worksheet.write('B%s' %(row), 'Invoice Number')
        worksheet.write('C%s' %(row), 'Invoice date')
        worksheet.write('D%s' %(row), 'Invoice Value')
        worksheet.write('E%s' %(row), 'Place Of Supply')
        worksheet.write('F%s' %(row), 'Reverse Charge')
        worksheet.write('G%s' %(row), 'Invoice Type')
        worksheet.write('H%s' %(row), 'E-Commerce GSTIN')
        worksheet.write('I%s' %(row), 'Rate')
        worksheet.write('J%s' %(row), 'Taxable Value')
        worksheet.write('K%s' %(row), 'Cess Amount')

        ls = []
        for obj in invoice_id:
            if obj.export_invoice == False and obj.partner_id.vat:
                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:
                        for line in rec.invoice_line_tax_ids:
                            if line.children_tax_ids:
                                if sum(line.children_tax_ids.mapped('amount')) == 1:
                                    ls.append(1)
                                if sum(line.children_tax_ids.mapped('amount')) == 2:
                                    ls.append(2)
                                if sum(line.children_tax_ids.mapped('amount')) == 5:
                                    ls.append(5)
                                if sum(line.children_tax_ids.mapped('amount')) == 18:
                                    ls.append(18)
                                if sum(line.children_tax_ids.mapped('amount')) == 28:
                                    ls.append(28)
                            else:
                                if line.amount == 1:
                                    ls.append(1)
                                if line.amount == 2:
                                    ls.append(2)
                                if line.amount == 5:
                                    ls.append(5)
                                if line.amount == 18:
                                    ls.append(18)
                                if line.amount == 28:
                                    ls.append(28)


        for obj in invoice_id:
            if obj.partner_id.vat:
                for rip in set(ls):
                    r=0
                    for rec in obj.invoice_line_ids:
                        if rec.invoice_line_tax_ids:
                            for line in rec.invoice_line_tax_ids:
                                if line.children_tax_ids:
                                    if sum(line.children_tax_ids.mapped('amount')) == rip:
                                        r+=rec.price_subtotal
                                else:
                                    if line.amount == rip:
                                        r+=rec.price_subtotal
                    if r == 0:
                        pass
                    else:
                        worksheet.write('A%s' %(new_row), obj.partner_id.vat)
                        worksheet.write('B%s' %(new_row), obj.number)
                        worksheet.write('C%s' %(new_row), obj.date_invoice)
                        worksheet.write('D%s' %(new_row), obj.amount_total)
                        worksheet.write_rich_string('E%s' %(new_row), str(obj.partner_id.state_id.state_code) + str("-") + str(obj.partner_id.state_id.name))
                        worksheet.write('F%s' %(new_row), 'N')
                        worksheet.write('G%s' %(new_row), '')
                        worksheet.write('H%s' %(new_row), '')
                        worksheet.write('I%s' %(new_row), rip)
                        worksheet.write('J%s' %(new_row), r)
                        worksheet.write('K%s' %(new_row), '')

                        new_row+=1
