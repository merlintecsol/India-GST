# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    # @api.multi
    @api.depends('price_unit', 'product_uom_qty', 'tax_id.tax_type', 'tax_id.type_tax_use','discount')
    def _compute_gst(self):
        cgst_total = 0
        sgst_total = 0
        igst_total = 0
        cgst_rate = 0
        sgst_rate = 0
        igst_rate = 0

        for rec in self:
            cgst_total = 0
            sgst_total = 0
            igst_total = 0
            for line in rec.tax_id:
                if line.tax_type == 'cgst' and line.type_tax_use == 'sale':
                    cgst_total = cgst_total + line.amount
                if line.tax_type == 'sgst' and line.type_tax_use == 'sale':
                    sgst_total = sgst_total + line.amount
                if line.tax_type == 'igst' and line.type_tax_use == 'sale':
                    igst_total = igst_total + line.amount
                if line.tax_type == 'cgst' and line.type_tax_use == 'purchase':
                    cgst_total = cgst_total + line.amount
                if line.tax_type == 'sgst' and line.type_tax_use == 'purchase':
                    sgst_total = sgst_total + line.amount
                if line.tax_type == 'igst' and line.type_tax_use == 'purchase':
                    igst_total = igst_total + line.amount
                cgst_rate = cgst_total/100
                sgst_rate = sgst_total/100
                igst_rate = igst_total/100

            base = rec.price_unit * (1 - (rec.discount or 0.0) / 100.0)
            rec.cgst = (base * rec.product_uom_qty) * cgst_rate
            rec.sgst = (base * rec.product_uom_qty) * sgst_rate
            rec.igst = (base * rec.product_uom_qty) * igst_rate
            rec.amount = (base * rec.product_uom_qty) + rec.cgst + rec.sgst + rec.igst
            # rec.gst_amount = gst_amt

    cgst = fields.Float(string='CGST', compute='_compute_gst', store=True)
    sgst = fields.Float(string='SGST', compute='_compute_gst')
    igst = fields.Float(string='IGST', compute='_compute_gst')
    amount = fields.Float(string='Amt. with Taxes', readonly=True, compute='_compute_gst')
