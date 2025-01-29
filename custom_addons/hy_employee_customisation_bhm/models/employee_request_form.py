from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeRequestForm(models.Model):
    _name = "employee.request.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Employee Request Form"
    _order = "requested_date desc"

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
        string="Requested By",
        required=True,
        default=lambda self: self.env.user.employee_id,
    )
    employe_manager_id = fields.Many2one(
        "hr.employee",
        string="Manager",
        related="employee_id.parent_id",
        store=True,
    )
    requested_date = fields.Datetime(
        string="Requested Date",
        required=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="User",
        related="employee_id.user_id",
        store=True,
    )
    purpose = fields.Char(
        string="Purpose",
        required=True,
    )
    summary = fields.Html(
        string="Summary",
    )
    attachment = fields.Binary(
        string="Attachment",
    )
    request_type_id = fields.Many2one(
        "employee.request.type",
        string="Request Type",
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
            ("rejected", "Rejected"),
        ],
        string="State",
        default="draft",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("employee.request.form")
        return super(EmployeeRequestForm, self).create(vals)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if not self.employee_id:
            raise UserError(_("Employee need to link with the logged in user."))

    def action_confirm(self):
        self._create_activity(self.user_id)
        self.write({"state": "submitted"})
        return True

    def action_approve(self):
        self.write({"state": "approved"})
        return True

    def action_reject(self):
        self.write({"state": "rejected"})
        return True

    def _create_activity(self, users):
        for user in users:
            self.activity_schedule(
                "hy_employee_customisation_bhm.mail_activity_request",
                user_id=user.id,
            )
