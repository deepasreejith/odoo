from odoo import models, fields


class VisaApplication(models.Model):
    _name ="visa.application"

    name = fields.Char("Name")
    age = fields.Integer("Age")
    gender = fields.Selection([('male','Male'),('female','Female')])
    date_of_birth = fields.Date("Date of Birth")