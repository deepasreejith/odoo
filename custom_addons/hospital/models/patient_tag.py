from odoo import fields,models,api,_

class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'

    name = fields.Char(string='Name',required=True,trim=False)
    active = fields.Boolean(string='Active',default=True,copy=False)
    color = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color 2')
    sequence = fields.Integer(string='sequence')

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)", self.name)
            default['sequence'] = 10
        return super(PatientTag, self).copy(default=default)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Name must be unique!'),
        ('check_sequence', 'check(sequence > 0)', 'sequence must be greater than 0'),
    ]