from odoo import fields,models,api
from odoo.exceptions import UserError

class Student(models.Model):
    _name = 'student.profile'
    _order = 'id desc'
   #  _log_access = False    this used to not create  create_date,create_uid,write_date,write_uid fields.

    stud_seq = fields.Integer(string='Sequence',default=0)
    name = fields.Char(string='Student Name',copy=False)
    image = fields.Image('Student Image')
    roll_no = fields.Char(string='Roll no')
    hobby_id = fields.Many2many('student.hobby',string='Hobbies',required=True)
    school_id = fields.Many2one('school.profile',string='School',
                                domain=[('school_type','=','public')]
                                )
    state = fields.Selection([('draft','Draft'),('progress','Progress'),('paid','Paid'),('done','Done')],string='States')

    is_virtual_school = fields.Boolean(related='school_id.is_virtual_class',string='Virtual School')
    currency_id = fields.Many2one('res.currency',string='Currency')
    student_fee = fields.Monetary(string='Student Fee')
    total_fee = fields.Float(string='Total Fee')
    ref_id = fields.Reference([('school.profile','School'),('account.move','Invoice'),],string='Reference') # reference field is a combination of many2one and selection field
    active = fields.Boolean(string='Active',default=True)
    bdate = fields.Date(string='Date of birth')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'please enter unique name'),
        ('total_fee_check', 'check(total_fee>100)', 'add total fee greater than 100')
    ]
    @api.model
    def _create_roll_no_sequences(self,param):
            for stud in self.search([('roll_no', '!=', False)]):
                stud.roll_no =param+'STD'+str(stud.id)

    def update_student_fee(self):
        return self.env['ir.actions.act_window']._for_xml_id('school.student_fee_update_form_view_wizard_action')
        # return {
        #     'type' : 'ir.actions.act_window',
        #     'res_model' : 'student.fee.update.wizard',
        #     'view_mode' : 'form',
        #     'target' : 'new'
        # }

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

    # def unlink(self):
    #     print("unlink method called")
    #     for stu in self:
    #         if stu.total_fee > 0:
    #             raise UserError(
    #                 "You can not deleted %s,Because it fee grater than zero."%(stu.name))
    #     rtn = super(Student, self).unlink()
    #     print(rtn)

    @api.model
    def default_get(self, field_list=[]):
        print("default_get method called")
        print(field_list)
        rtn = super(Student, self).default_get(field_list)
        rtn['name'] = 'Your Name'
        print(rtn)
        return rtn

    def spec_command6(self):
        ids = [1,2,3]
        self.write({'hobby_id': [(6, 0, ids)]})  # add to the manytomany field using spe commd

class Hobby(models.Model):
    _name = 'student.hobby'

    name = fields.Char(string='Hobby')