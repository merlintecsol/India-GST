# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
from datetime import date
from datetime import datetime, date
import odoo.addons.decimal_precision as dp
import re
class GstrB2CLXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, invoices):


        invoice_obj = self.env['check.date'].search([])[-1]
        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',invoice_obj.start_date),
                                                        ('date_invoice','<=',invoice_obj.end_date)])

        worksheet = workbook.add_worksheet('GSTR B2CL')
        worksheet.set_column('A:H',15)

        row = 1
        col = 0
        new_row = row + 1

        worksheet.write('A%s' %(row), 'Invoice Number')
        worksheet.write('B%s' %(row), 'Invoice date')
        worksheet.write('C%s' %(row), 'Invoice Value')
        worksheet.write('D%s' %(row), 'Place Of Supply')
        worksheet.write('E%s' %(row), 'Rate')
        worksheet.write('F%s' %(row), 'Taxable Value')
        worksheet.write('G%s' %(row), 'Cess Amount')
        worksheet.write('H%s' %(row), 'E-Commerce GSTIN')

        partner_state = self.env.user.company_id.partner_id.state_id.name

        ls = []
        for obj in invoice_id:
            if obj.partner_id.gstin_registered == False and obj.amount_total > 250000 and obj.partner_id.property_account_position_id.name == 'Inter State':
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
            if obj.partner_id.gstin_registered == False and obj.amount_total > 250000 and obj.partner_id.property_account_position_id.name == 'Inter State':
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
                            print '++++++++++++++++',obj.partner_id.name


                            worksheet.write('A%s' %(new_row), obj.number)
                            worksheet.write('B%s' %(new_row), date(year,mon,day).strftime('%d %b %Y'))
                            worksheet.write('C%s' %(new_row), obj.amount_total)
                            worksheet.write_rich_string('D%s' %(new_row), obj.partner_id.state_id.state_code + "-" + obj.partner_id.state_id.name)
                            worksheet.write('E%s' %(new_row), row[1])
                            worksheet.write('F%s' %(new_row), r)
                            worksheet.write('G%s' %(new_row), '')
                            worksheet.write('H%s' %(new_row), obj.partner_id.e_commerce_tin)

                            new_row+=1



GstrB2CLXlsx('report.account.gstr.b2cl.xlsx',
            'account.invoice')
