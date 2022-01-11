# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2020 Bernard K. Too<bernard.too@optima.co.ke>
"""
from odoo import fields, models


class res_currency(models.Model):
    _inherit = "res.currency"

    currency_name = fields.Char(
        "Currency Name", help="Currency full name e.g US Dollars"
    )
