from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = " estate property tag details"
    _order = "name"

    name = fields.Char(string='Name',required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('unique_property_tag_name', 'UNIQUE(name)', 'Property tag name must be unique.')
    ]