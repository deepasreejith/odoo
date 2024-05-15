from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = " estate property type details"

    name = fields.Char(string='Name',required=True)

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]