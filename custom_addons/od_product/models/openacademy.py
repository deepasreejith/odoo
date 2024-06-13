from odoo import models, fields, api

class Course(models.Model):
    _name = 'od_product.course'

    name = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users',ondelete = 'set null')
    session_ids = fields.One2many('od_product.session','course_id',string='Sessions')

class Session(models.Model):
    _name = 'od_product.session'

    name = fields.Char(string='Name',required=True)
    start_date = fields.Date(string='Start Date')
    duration = fields.Float(string='Duration')
    seats = fields.Integer(string='Seats')
    instructor_id = fields.Many2one('res.partner',string='Instructor')
    course_id = fields.Many2one('od_product.course',string='Course',required=True)
    attendees_id = fields.Many2many('res.partner',string='Attendees')