# -*- coding: utf-8 -*-
# Copyright 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.tools.translate import _


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    public_holiday_id = fields.Many2one(
        'hr.holidays.public.line',
        string="Public Holiday")

    @api.model
    def get_employee_calendar(self, employee):
        calendar = None
        if employee.resource_id.calendar_id:
            calendar = employee.resource_id.calendar_id.id
        return calendar

    @api.multi
    def holidays_validate(self):
        for holiday in self:
            if not holiday.holiday_type == 'employee':
                return super(HrHolidays, self).holidays_validate()

            try:
                res_id = self.env['ir.model.data'].get_object(
                    'hr_public_holidays_leaves', 'hr_public_holiday').id
            except ValueError:
                raise Warning(
                    _("Leave Type for Public Holiday not found!"))

            if holiday.holiday_status_id.id != res_id:
                return super(HrHolidays, self).holidays_validate()

            calendar = self.get_employee_calendar(holiday.employee_id)

            self.env['resource.calendar.leaves'].create({
                'name': holiday.name,
                'date_from': holiday.date_from,
                'date_to': holiday.date_to,
                'resource_id': holiday.employee_id.resource_id.id,
                'calendar_id': calendar,
                'holiday_id': holiday.id
            })
            holiday.state = 'validate'
