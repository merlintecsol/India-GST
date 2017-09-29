# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
import datetime
from datetime import datetime, date
import odoo.addons.decimal_precision as dp
import re
class GstrB2BXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, invoices):

        invoice_obj = self.env['check.date'].search([])[-1]
        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',invoice_obj.start_date),
                                                        ('date_invoice','<=',invoice_obj.end_date)])

        worksheet = workbook.add_worksheet('GSTR B2B')
        worksheet.set_column('A:K',15)

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
            if obj.flag_field == True and obj.export_invoice == False:

                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:

                        if rec.tax_desc == 'gst' and rec.gst_amount == 5:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'gst' and rec.gst_amount == 12:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'gst' and rec.gst_amount == 18:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'gst' and rec.gst_amount == 28:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'igst' and rec.gst_amount == 5:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'igst' and rec.gst_amount == 12:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'igst' and rec.gst_amount == 18:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'igst' and rec.gst_amount == 28:
                            ls.append([rec.tax_desc,rec.gst_amount])
                        if rec.tax_desc == 'none' and rec.gst_amount == 0:
                            ls.append([rec.tax_desc,rec.gst_amount])

        for obj in invoice_id:
            if obj.flag_field == True and obj.export_invoice == False:
                for row in set(map(tuple, ls)):
                    r = 0
                    for rec in obj.invoice_line_ids:
                        if rec.invoice_line_tax_ids:
                            if rec.tax_desc == row[0] and rec.gst_amount == row[1]:
                                r+=rec.price_subtotal
                        if r == 0:
                            pass
                        else:
                            line = re.sub('[-]', '', obj.date_invoice)
                            year = int(line[:4])
                            mon = int(line[4:6])
                            day = int(line[6:8])

                            worksheet.write('A%s' %(new_row), obj.partner_id.gstin)
                            worksheet.write('B%s' %(new_row), obj.number)
                            inv_date = obj.date_invoice
                            worksheet.write('C%s' %(new_row), date(year,mon,day).strftime('%d %b %Y'))
                            worksheet.write('D%s' %(new_row), obj.amount_total)
                            if obj.partner_id.state_id:
                                worksheet.write_rich_string('E%s' %(new_row), obj.partner_id.state_id.state_code + "-" + obj.partner_id.state_id.name)
                            else:
                                worksheet.write('E%s' %(new_row), '')
                            worksheet.write('F%s' %(new_row), 'N')
                            worksheet.write('G%s' %(new_row), obj.invoice_type)
                            worksheet.write('I%s' %(new_row), row[1])
                            worksheet.write('J%s' %(new_row), r)
                            worksheet.write('K%s' %(new_row), '')

                            new_row+=1



GstrB2BXlsx('report.account.gstr.b2b.xlsx',
            'account.invoice')




