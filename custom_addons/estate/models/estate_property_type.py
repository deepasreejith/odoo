from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = " estate property type details"

    name = fields.Char(string='Name',required=True)
