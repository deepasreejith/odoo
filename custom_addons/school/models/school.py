from odoo import fields,models,api


class SchoolProfile(models.Model):
    _name = 'school.profile'
    _rec_name = 'name'

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

    _sql_constraints = [
        ('name_unique','unique (name)','please enter unique school name'),
    ]

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

    @api.depends('school_type', 'name')
    def _compute_display_name(self):
        for school in self:
            name = school.name or ''
            if school.school_type:
                school.display_name = f"{name} ({school.school_type})"
            else:
                school.display_name = name  # Fallback if school_type is not set

    def name_get(self):  # it will override rec_name
        result = []
        for record in self:
            name = record.name or "Unnamed School"  # Example: Handle empty names
            if record.school_type:
                name = f"{name} ({record.school_type})"
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None,order=None ):
        if name:
            domain = ['|','|','|',('name',operator,name),('email',operator,name),('school_type',operator,name)]
        return super()._name_search(name, domain, operator, limit,order)

    def create_stu_spec_command(self):
        print("create_stu_spec_command called")
        self.create({'name':'new modern school','student_ids':[(0,0,{'name':'std1','total_fee':434,}),
                                                               (0,0,{'name':'std2','total_fee':334,}),
                                                               (0,0,{'name':'std3','total_fee':474,})
                                                               ]})
    def spec_command1(self):
        vals = {'student_ids':[]}
        for stu in self.student_ids:
            vals['student_ids'].append([1,stu.id,{'name':stu.name+" Name",
                                                  'total_fee':5000,
                                                  'student_fee':400}])
        self.write(vals)
    def spec_command2(self):
        self.write({'student_ids':[(2,7,0),(2,5,0)]})  # permenently delete
    def spec_command3(self):
        self.write({'student_ids': [(3, 10, 0)]})  #not permenently delete ,it delete only from the list
    def spec_command4(self):
        self.write({'student_ids': [(4, 10, 0)]}) # add to the list using spe commd
    def spec_command5(self):
        self.write({'student_ids': [(5, 0, 0)]}) # it delete all from list.but not permenently delete