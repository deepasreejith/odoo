from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = 'od_product.course'

    name = fields.Char(string='Name', required=True,translate=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users', ondelete='set null')
    session_ids = fields.One2many('od_product.session', 'course_id', string='Sessions')

    _sql_constraints = [
        ('check_name_and_description', 'CHECK(name != description)',
         'The name and description are not make same.'),
        ('name_unique', 'unique(name)',
         'unique title!'),
    ]


class Session(models.Model):
    _name = 'od_product.session'

    name = fields.Char(string='Name', required=True,translate=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    duration = fields.Float(string='Duration')
    seats = fields.Integer(string='Seats')
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    course_id = fields.Many2one('od_product.course', string='Course', required=True)
    attendees_ids = fields.Many2many('res.partner', string='Attendees')
    taken_seats = fields.Float(string='Taken Seats', compute='_compute_taken_seats')
    active = fields.Boolean(default=True)

    @api.constrains('instructor_id','attendees_ids')
    def check_instructor_as_attendees(self):
        for rec in self:
            if rec.instructor_id.id in rec.attendees_ids.ids:
                raise ValidationError(_("Cannot set attendees as instructor."))

    @api.onchange('attendees_ids', 'seats')
    def _onchange_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': 'Something bad happend',
                    'message': 'seats not add negative'
                }
            }
        if self.seats < len(self.attendees_ids):
            return {
                'warning': {
                    'title': 'Something bad happend',
                    'message': 'you cannot add more attendees than seats'
                }
            }

    @api.depends('attendees_ids', 'seats')
    def _compute_taken_seats(self):
        for session in self:
            if session.seats == 0:
                session.taken_seats = 0
            else:
                session.taken_seats = (len(session.attendees_ids) / session.seats) * 100
