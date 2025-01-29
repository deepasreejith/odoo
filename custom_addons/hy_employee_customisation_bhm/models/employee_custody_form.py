from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeCustodyForm(models.Model):
    _name = "employee.custody.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Custody Form"

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
    requested_date = fields.Date(
        string="Requested Date",
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
        "employee.custody.form.line",
        "form_id",
        string="Lines",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("employee.custody.form")
        return super(EmployeeCustodyForm, self).create(vals)

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
                "hy_employee_customisation_bhm.mail_activity_employee_custody",
                user_id=user.id,
            )


class EmployeeCustodyFormLine(models.Model):
    _name = "employee.custody.form.line"
    _description = "Employee Custody Form Line"

    form_id = fields.Many2one(
        "employee.custody.form",
        string="Form",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="custody Details",
        required=True,
    )
    custody_type = fields.Char(
        string="Custody Type (Char)",
    )
    custody_type_id = fields.Many2one(
        "employee.custody.type",
        string="Custody Type",
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
    )
    serial_number = fields.Char(
        string="Serial Number",
    )
