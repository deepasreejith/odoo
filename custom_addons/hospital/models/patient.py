from odoo import fields,models,api
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name',tracking=True)
    date_of_birth = fields.Date(string='Date of Birth')
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age',compute='_compute_age',tracking=True) # computed fields are nostored field.if we want to sore,store=True
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string='Gender',tracking=True)
    active = fields.Boolean(string='Archive',default=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

