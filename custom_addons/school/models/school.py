from odoo import fields,models,api


class SchoolProfile(models.Model):
    _name = 'school.profile'

    name = fields.Char(string='School Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')