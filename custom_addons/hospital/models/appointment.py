from odoo import fields,models,api

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient',string='Patient')
    appointment_time = fields.Datetime(string='Appointment Time',default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date',default=fields.Date.context_today)
    gender = fields.Selection(related='patient_id.gender')
    ref = fields.Char(string='Reference',help='Reference from  patient record')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft','Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],string='Status',default='draft',required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines','appointment_id',string='Pharmacy Line')
    hide_sales_price = fields.Boolean(string='Hide sale Price')
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def object_button(self):
        print("Object button!!!!!!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'button clicked',
                'type': 'rainbow_man',
            }
        }
    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product',required=True)
    price_unit = fields.Float(string='Price',related='product_id.list_price')
    qty = fields.Integer(string='Quantity',default=1)
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')