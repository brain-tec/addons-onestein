# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def create(self, vals):
        if not self.env.context.get('skip_sequence_creation', False):
            company_id = vals.get('company_id', False)
            if not company_id:
                company_id = self.env.user.company_id.id
            number = self.env['ir.sequence'].with_context(
                force_company=company_id
            ).next_by_code('account.analytic.account')
            vals['code'] = number or '/'
        return super().create(vals)

    _sql_constraints = [
        ('code',
         'unique (code,company_id)',
         'Sequence must be unique per company!')
    ]
