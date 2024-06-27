from odoo import fields,models,api
from odoo.exceptions import UserError

class Student(models.Model):
    _name = 'student.profile'

    name = fields.Char(string='Student Name',copy=False)
    hobby_id = fields.Many2many('student.hobby',string='Hobbies',required=True)
    school_id = fields.Many2one('school.profile',string='School')
    is_virtual_school = fields.Boolean(related='school_id.is_virtual_class',string='Virtual School')
    currency_id = fields.Many2one('res.currency',string='Currency')
    student_fee = fields.Monetary(string='Student Fee')
    total_fee = fields.Float(string='Total Fee')
    ref_id = fields.Reference([('school.profile','School'),('account.move','Invoice'),],string='Reference') # reference field is a combination of many2one and selection field
    active = fields.Boolean(string='Active',default=True)

    @api.model
    def create(self,vals):
        # print(vals)
        # vals['active'] = True
        # print(vals)
        print("create method called")
        rtn = super(Student,self).create(vals)
        return rtn

    def write(self,vals):
        # print(vals)
        # vals['total_fee'] = 0
        # print(vals)
        print("write method called")
        rtn = super(Student,self).write(vals)
        return rtn

    def copy(self,default={}):
        print("copy method called")
        default['name'] = "copy("+self.name+")"
        rtn = super(Student, self).copy(default=default)
        rtn.total_fee = 500
        return rtn

    def unlink(self):
        print("unlink method called")
        for stu in self:
            if stu.total_fee > 0:
                raise UserError(
                    "You can not deleted %s,Because it fee grater than zero."%(stu.name))
        rtn = super(Student, self).unlink()
        print(rtn)

    @api.model
    def default_get(self, field_list=[]):
        print("default_get method called")
        print(field_list)
        rtn = super(Student, self).default_get(field_list)
        rtn['name'] = 'Your Name'
        print(rtn)
        return rtn

class Hobby(models.Model):
    _name = 'student.hobby'

    name = fields.Char(string='Hobby')