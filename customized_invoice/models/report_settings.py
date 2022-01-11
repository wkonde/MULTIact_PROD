# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2020 Bernard K. Too<bernard.too@optima.co.ke>
"""
from odoo import api, fields, models


class TemplateSettings(models.Model):
    _name = "report.template.settings"
    _description = "Professional Invoice & Sales Order Settings"

    @api.model
    def _default_so_template(self):
        def_tpl = self.env["ir.ui.view"].search(
            [
                ("key", "like", "customized_invoice.SO\_%\_document"),
                ("type", "=", "qweb"),
            ],
            order="key asc",
            limit=1,
        )
        return def_tpl or self.env.ref("sale.report_saleorder_document")

    @api.model
    def _default_inv_template(self):
        def_tpl = self.env["ir.ui.view"].search(
            [
                ("key", "like", "customized_invoice.INVOICE\_%\_document"),
                ("type", "=", "qweb"),
            ],
            order="key asc",
            limit=1,
        )
        return def_tpl or self.env.ref("account.report_invoice_document")

    name = fields.Char(
        "Name of Style", required=True, help="Give a unique name for this report style"
    )
    template_inv = fields.Many2one(
        "ir.ui.view",
        "Invoice",
        default=_default_inv_template,
        domain="[('type', '=', 'qweb'), ('key', 'like', 'customized_invoice.INVOICE\_%\_document' )]",
        required=False,
    )
    template_so = fields.Many2one(
        "ir.ui.view",
        "Order/Quote",
        default=_default_so_template,
        domain="[('type', '=', 'qweb'), ('key', 'like', 'customized_invoice.SO\_%\_document' )]",
        required=False,
    )

    logo = fields.Binary(
        "Report Logo",
        attachment=True,
        help="This field holds the image used as logo for the reports, if non is uploaded, the company logo will be used",
    )
    footer_logo = fields.Binary(
        "Footer Logo",
        attachment=True,
        help="This field holds the image used as footer logo for the reports, if non is uploaded and footer logo is enabled then the company logo will be used",
    )
    odd = fields.Char(
        "Odd parity Color",
        size=7,
        required=True,
        default="#F2F2F2",
        help="The background color for Odd invoice lines in the invoice",
    )
    even = fields.Char(
        "Even parity Color",
        size=7,
        required=True,
        default="#FFFFFF",
        help="The background color for Even invoice lines in the invoice",
    )
    theme_color = fields.Char(
        "Theme Color",
        size=7,
        required=True,
        default="#F07C4D",
        help="The Main Theme color of the invoice. Normally this\
                     should be one of your official company colors",
    )
    text_color = fields.Char(
        "Text Color",
        size=7,
        required=True,
        default="#6B6C6C",
        help="The Text color of the invoice. Normally this\
                     should be one of your official company colors or default HTML text color",
    )
    name_color = fields.Char(
        "Company Name Color",
        size=7,
        required=True,
        default="#F07C4D",
        help="The Text color of the Company Name. Normally this\
                     should be one of your official company colors or default HTML text color",
    )
    cust_color = fields.Char(
        "Customer Name Color",
        size=7,
        required=True,
        default="#F07C4D",
        help="The Text color of the Customer Name. Normally this\
                     should be one of your official company colors or default HTML text color",
    )
    theme_txt_color = fields.Char(
        "Theme Text Color",
        size=7,
        required=True,
        default="#FFFFFF",
        help="The Text color of the areas bearing the theme color. Normally this should NOT be the same color as the\
                            theme color. Otherwise the text will not be visible",
    )

    header_font = fields.Selection(
        [(str(x), str(x)) for x in range(1, 51)],
        string="Header Font(px):",
        default="10",
        required=True,
    )
    body_font = fields.Selection(
        [(str(x), str(x)) for x in range(1, 51)],
        string="Body Font(px):",
        default="10",
        required=True,
    )
    footer_font = fields.Selection(
        [(str(x), str(x)) for x in range(1, 51)],
        string="Footer Font(px):",
        default="8",
        required=True,
    )
    font_family = fields.Char("Font Family:", default="sans-serif", required=True)
    aiw_report = fields.Boolean(
        "Enable Amount in Words",
        default=True,
        help="Check this box to enable the display of amount in words in the invoice/quote/sale order reports",
    )
    show_img = fields.Boolean(
        "Enable product Image",
        default=True,
        help="Check this box to display product image in Sales Order, Quotation, Invoice and Delivery Note",
    )
    show_footer_logo = fields.Boolean(
        "Enable Footer Logo",
        default=True,
        help="Check this box to display footer logo in the reports",
    )
    footer = fields.Boolean(
        "Enable footer",
        default=True,
        help="Check this box to enable footer in your reports. You may want to disable footer if you are using a watermark PDF with a footer content already",
    )
    header = fields.Boolean(
        "Enable header",
        default=True,
        help="Check this box to enable header in your reports. \nYou may want to disable header if\
                  you are using a watermark PDF with a header content already",
    )
