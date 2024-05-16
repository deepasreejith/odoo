from odoo import fields, models,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = " estate property type details"
    _order = "sequence,name"

    name = fields.Char(string='Name',required=True)
    property_ids = fields.One2many('estate.property','property_type_id')
    sequence = fields.Char(string='Ref', default=1)

    _sql_constraints = [
        ('unique_property_type_name', 'UNIQUE(name)', 'Property type name must be unique.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'estate.property.type')
        return super(EstatePropertyType, self).create(vals_list)