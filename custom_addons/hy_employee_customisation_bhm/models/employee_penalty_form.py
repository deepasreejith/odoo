from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeePenaltyForm(models.Model):
    _name = "employee.penalty.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Penalty Form"
    _order = "date desc"

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
    date = fields.Date(
        string="Date",
        required=True,
    )
    summary = fields.Html(
        string="Summary",
    )
    warning_type_id = fields.Many2one(
        "penalty.warning.type",
        string="Warning",
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
        "employee.penalty.form.line",
        "form_id",
        string="Lines",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("employee.penalty.form")
        return super(EmployeePenaltyForm, self).create(vals)

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
                "hy_employee_customisation_bhm.mail_activity_penalty",
                user_id=user.id,
            )


class EmployeePenaltyFormLine(models.Model):
    _name = "employee.penalty.form.line"
    _description = "Employee Penalty Form Line"

    form_id = fields.Many2one(
        "employee.penalty.form",
        string="Form",
        ondelete="cascade",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
    )
    type_of_violation = fields.Char(
        string="Type of Violation",
        required=True,
    )
    no_of_repetition = fields.Integer(
        string="No. of Repetition",
    )
    penalty = fields.Char(
        string="Penalty",
    )
    total_deduction = fields.Float(
        string="Total Deduction",
    )
