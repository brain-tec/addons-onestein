# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    analytic_type_id = fields.Many2one(
        'account.analytic.type',
        string='Type')
    child_ids = fields.One2many(
        'account.analytic.account',
        'parent_id',
        string="Children")
    parent_id = fields.Many2one(
        'account.analytic.account',
        string='Parent',
        domain=[('analytic_type_id.is_view', '=', True)])
