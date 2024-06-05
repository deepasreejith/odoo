from odoo import fields, models, api, _
from datetime import date
from odoo.exceptions import ValidationError
from  dateutil import relativedelta
class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', tracking=1)
    image = fields.Image(string='Image')
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age', compute='_compute_age',inverse='_inverse_compute_age',
                         search='search_age', tracking=10)  # computed fields are nostored field.if we want to sore,store=True
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',
                              tracking=15)
    active = fields.Boolean(string='Archive', default=True)
    tag_ids = fields.Many2many('patient.tag', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count',compute = '_compute_appointment_count',store=True)
    appointment_ids = fields.One2many('hospital.appointment','patient_id',string='Appointment id')
    parent_name = fields.Char(string='Parent')
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string='Marital Status',
                              tracking=True)
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string='Birthday ?',compute='_compute_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='website')
    @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #     for rec in self:
    #         print(rec.id)
    #         rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',rec.id)])
    # using rea_group orm method below:
    def _compute_appointment_count(self):
        appointment_group = self.env['hospital.appointment'].read_group(domain=[],fields=['patient_id'],groupby=['patient_id'])

        for appoinment in appointment_group:
            patient_id = appoinment.get('patient_id')[0]
            patient_rec = self.browse(patient_id)
            patient_rec.appointment_count = appoinment['patient_id_count']
            self = self - patient_rec
        self.appointment_count = 0

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
    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
            return

    def search_age(self,operator,value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_year = date_of_birth.replace(day=1,month=1)
        end_year = date_of_birth.replace(day=31, month=12)
        print(start_year)
        print(end_year)

        return [('date_of_birth','>=',start_year),('date_of_birth','<=',end_year)]

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
    @api.depends('date_of_birth')
    def _compute_birthday(self):
        print("---------------------")
        is_birthday = False
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday
            print(rec.is_birthday)

    def action_view_appointment(self):
        return {
            'name': _('Appointment'),
            'view_mode': 'tree,form',
            'domain': [('patient_id','=',self.id)],
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id':self.id},
        }