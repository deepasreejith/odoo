from odoo import models, fields, api, _


class EmployeeTask(models.Model):
    _name = "employee.task"
    _description = "Employee Task"

    name = fields.Char(string="Task Name", required=True)
    description = fields.Text(string="Description")
    employee_id = fields.Many2one("hr.employee", string="Employee")
