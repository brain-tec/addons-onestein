# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Netherlands BTW Statement',
    'version': '10.0.1.0.0',
    'category': 'Localization',
    'license': 'AGPL-3',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'website': 'http://www.onestein.eu',
    'depends': [
        'account_tax_balance',
        'l10n_nl',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/l10n_nl_vat_statement.xml',
    ],
    'installable': True,
}
