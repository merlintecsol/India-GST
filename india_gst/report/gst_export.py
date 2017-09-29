# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
from datetime import date
from datetime import datetime, date
import odoo.addons.decimal_precision as dp
import re
class GstrExportXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, invoices):

        invoice_obj = self.env['check.date'].search([])[-1]
        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',invoice_obj.start_date),
                                                        ('date_invoice','<=',invoice_obj.end_date)])

        worksheet = workbook.add_worksheet('GSTR Export Invoices')
        worksheet.set_column('A:I',15)

        row = 1
        col = 0
        new_row = row + 1

        worksheet.write('A%s' %(row), 'Export Type')
        worksheet.write('B%s' %(row), 'Invoice Number')
        worksheet.write('C%s' %(row), 'Invoice Date')
        worksheet.write('D%s' %(row), 'Invoice Value')
        worksheet.write('E%s' %(row), 'Port Code')
        worksheet.write('F%s' %(row), 'Shipping Bill No.')
        worksheet.write('G%s' %(row), 'Shipping Bill Date')
        worksheet.write('H%s' %(row), 'Rate')
        worksheet.write('I%s' %(row), 'Taxable Value')

        partner_state = self.env.user.company_id.partner_id.state_id.name

        ls=[]
        for obj in invoice_id:
            if obj.export_invoice == True:

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
            if obj.export_invoice == True:
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


                            worksheet.write('A%s' %(new_row), obj.export_type)
                            worksheet.write('B%s' %(new_row), obj.number)
                            worksheet.write('C%s' %(new_row), date(year,mon,day).strftime('%d %b %Y'))
                            worksheet.write('D%s' %(new_row), obj.amount_total)
                            worksheet.write('E%s' %(new_row), obj.port_code.name)
                            worksheet.write('F%s' %(new_row), obj.ship_bill_no)
                            worksheet.write('G%s' %(new_row), obj.ship_bill_date)
                            worksheet.write('H%s' %(new_row), row[1])
                            worksheet.write('I%s' %(new_row), r)

                            new_row+=1


GstrExportXlsx('report.account.gstr.export.xlsx',
            'account.invoice')
