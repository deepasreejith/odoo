from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeSalaryForm(models.Model):
    _name = "employee.salary.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Salary Form"

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Assigned Employee",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="User",
        related="employee_id.user_id",
        store=True,
    )
    note = fields.Html(
        string="Note",
    )
    bank_name = fields.Char(
        string="Bank Name",
        required=True,
    )
    iban = fields.Char(
        string="IBAN",
        required=True,
    )
    requested_date = fields.Date(
        string="Requested Date",
        required=True,
    )
    date_from = fields.Date(
        string="Date From",
        required=True,
    )
    date_to = fields.Date(
        string="Date To",
        required=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        index=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
        ],
        string="State",
        default="draft",
    )
    line_ids = fields.One2many(
        "employee.salary.form.line",
        "form_id",
        string="Lines",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("employee.salary.form")
        return super(EmployeeSalaryForm, self).create(vals)

    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        if self.employee_id and not self.employee_id.user_id:
            raise UserError(_("Please assign a user to the employee."))

    def action_confirm(self):
        self._create_activity(self.user_id)
        self.write({"state": "submitted"})
        return True

    def action_approve(self):
        self.write({"state": "approved"})
        return True

    def _create_activity(self, users):
        for user in users:
            self.activity_schedule(
                "hy_employee_customisation_bhm.mail_activity_employee_salary",
                user_id=user.id,
            )


class EmployeeSalaryFormLine(models.Model):
    _name = "employee.salary.form.line"
    _description = "Employee salary Form Line"

    form_id = fields.Many2one(
        "employee.salary.form",
        string="Form",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="Salary Details",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )
