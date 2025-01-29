from odoo import models, fields, api, _


class EmployeeRequestType(models.Model):
    _name = "employee.request.type"
    _description = "Employee Request Type"

    name = fields.Char(string="Name", required=True)
