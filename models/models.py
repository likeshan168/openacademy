# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Course(models.Model):
    _name = 'openacademy.course'
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one(
        "res.users", ondelete="set null", index=True, string="Responsible")
    session_ids = fields.One2many(
        "openacademy.session", 'course_id', string="Sessions")
    _sql_constraints = [
        (
            'name_description_check',
            'CHECK(name!=description)',
            'The title of the course should not be the description'
        ),
        (
            'uniqe_name',
            'UNIQUE(name)',
            'The title of the course must be unique'
        )
    ]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count([
            ('name', '=like', _(u"Copy of {}%".format(self.name)))
        ])
        if not copied_count:
            new_name = _(u"Copy of {}".format(self.name))
        else:
            new_name = _(u"Copy of {} ({})".format(self.name, copied_count))
        default['name'] = new_name
        return super(Course, self).copy(default)


class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char(required=True)

    startdate = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), string="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()
    instructor_id = fields.Many2one('res.partner', string=_("Instructor"), domain=[
                                    '|', ('instructor', '=', True), ('category_id.name', 'ilike', 'teacher')])
    course_id = fields.Many2one(
        "openacademy.course", string="Course", required=True, ondelete="cascade")
    attender_ids = fields.Many2many("res.partner", string="Attenders")
    taken_seats = fields.Float(string="Taken Seats", compute="_compute_seats")
    end_date = fields.Date(string="End Date", store=True,
                           compute="_get_end_date", inverse="_set_end_date")
    hours = fields.Float(string="Duration in hours",
                         compute="_get_hours", inverse="_set_hours")
    attendees_count = fields.Integer(
        string="Attender Count", compute="_get_attender_count", store=True)
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),
    ])

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_confirm(self):
        self.state = 'confirmed'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.depends('attender_ids')
    def _get_attender_count(self):
        for r in self:
            r.attendees_count = len(r.attender_ids)

    @api.depends('duration')
    def _get_hours(self):
        for r in self:
            r.hours = r.duration * 24

    def _set_hours(self):
        for r in self:
            r.duration = r.hours / 24

    @api.multi
    def _compute_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.00
            else:
                r.taken_seats = 100 * len(r.attender_ids) / r.seats

    @api.onchange('seats', 'attender_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _('Incorrect seats value'),
                    'message': _('The number of avaliable seats may not be negative')
                }
            }
        if self.seats < len(self.attender_ids):
            return {
                'warning': {
                    'title': _('Too many attenders'),
                    'message': _('increase seats or remove excess attenders')
                }
            }

    @api.constrains('seats')
    def _check_seats(self):
        for r in self:
            if r.seats < 0:
                raise ValidationError(_("The number of seats is invalid"))

    @api.constrains('instructor_id', 'attender_ids')
    def _check_instructor_not_in_attenders(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attender_ids:
                raise ValidationError(
                    _("A session's instructor cannot be an attender"))

    @api.depends('startdate', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.startdate and r.duration):
                r.end_date = r.startdate
                continue
            start = fields.Datetime.from_string(r.startdate)
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.startdate and r.duration):
                continue
            start_date = fields.Datetime.from_string(r.startdate)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - start_date).days + 1
