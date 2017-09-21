# -*- coding: utf-8 -*-
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
import xlsxwriter
from datetime import date
from datetime import datetime, date
class GstrB2CSXlsx(ReportXlsx):
    def generate_xlsx_report(self, workbook, data, invoices):


        invoice_obj = self.env['check.date'].search([])[-1]
        invoice_id = self.env['account.invoice'].search([
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',invoice_obj.start_date),
                                                        ('date_invoice','<=',invoice_obj.end_date)])

        worksheet = workbook.add_worksheet('GSTR B2CS')
        worksheet.set_column('A:H',15)

        row = 1
        col = 0
        new_row = row + 1

        worksheet.write('A%s' %(row), 'Type')
        worksheet.write('B%s' %(row), 'Place Of Supply')
        worksheet.write('C%s' %(row), 'Rate')
        worksheet.write('D%s' %(row), 'Taxable Value')
        worksheet.write('E%s' %(row), 'Cess Amount')
        worksheet.write('F%s' %(row), 'E-Commerce GSTIN')

        partner_state = self.env.user.company_id.partner_id.state_id.name


        ls = []
        for obj in invoice_id:
             if obj.partner_id.gstin_registered == False and ((obj.amount_total <= 250000 and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State'):
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

        pot = []
        check = []
        for obj in invoice_id:
            if obj.partner_id.gstin_registered == False and ((obj.amount_total <= 250000 and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State'):
                if rec.invoice_line_tax_ids:
                    for row in set(map(tuple, ls)):
                        r = 0
                        for rec in obj.invoice_line_ids:
                            if rec.tax_desc == row[0] and rec.gst_amount == row[1]:
                                r+=rec.price_subtotal
                        if r == 0:
                            pass
                        else:
                            if obj.partner_id.e_commerce == True:
                                pot.append(['E',obj.partner_shipping_id.state_id.state_code + "-" + obj.partner_shipping_id.state_id.name,row[1],r,obj.partner_id.e_commerce_tin])
                                check.append(['E',str(obj.partner_shipping_id.state_id.state_code + "-" + obj.partner_shipping_id.state_id.name),row[1]])
                            else:
                                pot.append(['OE',obj.partner_shipping_id.state_id.state_code + "-" + obj.partner_shipping_id.state_id.name,row[1],r])
                                check.append(['OE',str(obj.partner_shipping_id.state_id.state_code + "-" + obj.partner_shipping_id.state_id.name),row[1]])


        for row in set(map(tuple, check)):
            l = 0
            d =''
            for rec in pot:
                if row[0] == rec[0] and row[1] == rec[1] and row[2] == rec[2]:
                    l+=rec[3]
                    if len(rec) == 5:
                        d=rec[4]
                    else:
                        d=''

            worksheet.write('A%s' %(new_row), row[0])
            worksheet.write('B%s' %(new_row), row[1])
            worksheet.write('C%s' %(new_row), row[2])
            worksheet.write('D%s' %(new_row), l)
            worksheet.write('E%s' %(new_row), '')
            worksheet.write('F%s' %(new_row), d)

            new_row+=1



GstrB2CSXlsx('report.account.gstr.b2cs.xlsx','account.invoice')
