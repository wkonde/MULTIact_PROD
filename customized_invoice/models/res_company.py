# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2020 Bernard K. Too<bernard.too@optima.co.ke>
"""
from odoo import fields, models


class ReportDefaultSettings(models.Model):
    _inherit = ["res.company"]

    facebook = fields.Char("Facebook ID")
    twitter = fields.Char("Twitter Handle")
    youtube = fields.Char("YouTube ID")

    df_style = fields.Many2one(
        "report.template.settings",
        "Default Style For All Reports",
        help="This is the report style that will be the default for any report which belongs to a partner who does not have a specific reports style defined. It is also the default style for new partners, unless you assign him/her a different reports style",
    )
