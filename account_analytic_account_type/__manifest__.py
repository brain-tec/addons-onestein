# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Account Analytic Account Type',
    'summary': 'Adds a Type field in the Analytic Account',
    'author': 'Onestein',
    'website': 'https://www.onestein.eu',
    'category': 'Accounting',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'analytic',
        'account',  # for menuitem Analytic Accounting
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic_account.xml',
        'views/account_analytic_type.xml',
    ],
}
