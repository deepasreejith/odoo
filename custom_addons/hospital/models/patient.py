from odoo import fields,models,api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string='Name',tracking=True)
    ref = fields.Char(string='Reference')
    age = fields.Integer(string='Age',tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string='Gender',tracking=True)
    active = fields.Boolean(string='Archive',default=True)