# -*- coding: utf-8 -*-
{

    'name': 'India-GST',
    'description': "Goods & Service-Tax.",
    'version': '1.0.1',
    'author': 'Merlin Tecsol Pvt. Ltd.',
    'website': 'http://www.merlintecsol.com',
    'license': 'AGPL-3',
    'depends': ['sale','purchase','account_accountant','report_xlsx'],
    'data': [
        "views/gst_view.xml",
        "views/gst_sale_view.xml",
        "views/gst_purchase_view.xml",
        "data/tax_data.xml",
        "data/res.country.state.csv",
        "data/fiscal_data.xml",
        "report/gst_sales_invoice_pdf.xml",
        "report/gst_invoice_pdf.xml",
        "report/gst_invoice.xml",
        'report/gst_b2b.xml',
        'wizard/gstr_b2b_wizard.xml',
        'wizard/gstr_b2cl_wizard.xml',
        'report/gst_b2cl_report.xml',
        'wizard/gstr_b2cs_wizard.xml',
        'report/gst_b2cs_report.xml',
        'wizard/gstr_hsn_wizard.xml',
        'report/gst_hsn_report.xml',
        'report/gst_export_report.xml',
        'views/port_code.xml',
        'wizard/gstr_export_wizard.xml',
    ]
}