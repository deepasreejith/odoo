from odoo import fields, models, api, _
from datetime import date
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    image = fields.Image(string='Image')
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age', compute='_compute_age',
                         tracking=True)  # computed fields are nostored field.if we want to sore,store=True
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',
                              tracking=True)
    active = fields.Boolean(string='Archive', default=True)
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count',compute = '_compute_appointment_count',store=True)
    appointment_ids = fields.One2many('hospital.appointment','patient_id',string='Appointment id')
    parent_name = fields.Char(string='Parent')
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string='Marital Status',
                              tracking=True)
    partner_name = fields.Char(string='Partner Name')
    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            print(rec.id)
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',rec.id)])
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('You entered date of birth is not valid.'))

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.ondelete(at_uninstall=False)
    def check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError('This patient has appointments')
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):

        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).write(vals)

    def name_get(self):

        return [(record.id,'%s %s' %(record.ref,record.name)) for record in self]

    def action_done(self):
        print("test")
        return