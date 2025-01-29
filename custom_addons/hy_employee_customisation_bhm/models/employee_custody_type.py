from odoo import fields, models


class EmployeeCustodyType(models.Model):
    _name = "employee.custody.type"
    _description = "Employee Custody Type"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
