# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2020 Bernard K. Too<bernard.too@optima.co.ke>
"""
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    delivery_instructions = fields.Text("Delivery Instructions")
    style = fields.Many2one(
        "report.template.settings",
        "Reports Style",
        help="Select a style to use when printing reports for this customer",
        default=lambda self: self.env.user.company_id.df_style,
    )
