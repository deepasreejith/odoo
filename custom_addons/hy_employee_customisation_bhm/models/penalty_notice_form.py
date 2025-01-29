from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PenaltyNoticeForm(models.Model):
    _name = "penalty.notice.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Penalty Notice Form"

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
    request_date = fields.Date(
        string="Request Date",
        required=True,
        default=fields.Date.today,
    )
    note = fields.Html(
        string="Note",
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
        "penalty.notice.form.line",
        "form_id",
        string="Lines",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("penalty.notice.form")
        return super(PenaltyNoticeForm, self).create(vals)

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
                "hy_employee_customisation_bhm.mail_activity_penalty_notice",
                user_id=user.id,
            )


class PenaltyNoticeFormLine(models.Model):
    _name = "penalty.notice.form.line"
    _description = "Penalty Notice Form Line"

    form_id = fields.Many2one(
        "penalty.notice.form",
        string="Form",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="Penalty Notice",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )
