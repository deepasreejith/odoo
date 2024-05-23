from odoo import fields,models,api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']

    patient_id = fields.Many2one('hospital.patient',string='Patient')
    appointment_time = fields.Datetime(string='Appointment Time',default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date',default=fields.Date.context_today)
    gender = fields.Selection(related='patient_id.gender')