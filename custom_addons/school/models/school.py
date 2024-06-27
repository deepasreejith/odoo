from odoo import fields,models,api


class SchoolProfile(models.Model):
    _name = 'school.profile'

    name = fields.Char(string='School Name',copy=False)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    is_virtual_class = fields.Boolean(string='virtual class is support?')
    result = fields.Float(string='Result')
    address = fields.Text(string='Address')
    establish_date = fields.Date(string='Established Date')
    open_date = fields.Datetime(string='Open Date')
    school_type = fields.Selection([('public','Public School'),('private','Private School')],string='Type of school')
    documents = fields.Binary(string='Documents')
    document_name = fields.Char(string='File Name')
    school_image = fields.Image(string='Upload school image' ,max_width = 10, max_height=10)
    school_description = fields.Html(string='School Description')
    student_ids = fields.One2many('student.profile','school_id',string='Students')
    auto_rank = fields.Integer(string='Rank',compute='_auto_rank')

    @api.depends('school_type')
    def _auto_rank(self):
        for rec in self:
            if rec.school_type == 'private':
                rec.auto_rank = 50
            elif rec.school_type == 'public':
                rec.auto_rank = 100
            else:
                rec.auto_rank = 0

    @api.model
    def name_create(self, name):
        print("name_create method called")
        # rtn = super(SchoolProfile,self).name_create(name)
        # return rtn
        rtn = self.create({'name':name,'email':'abc@gmail.com'})
        return rtn.id, rtn.display_name


