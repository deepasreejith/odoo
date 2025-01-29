from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TripAllowanceForm(models.Model):
    _name = "trip.allowance.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Trip Allowance Form"

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
    departure_date = fields.Date(
        string="Departure Date",
        required=True,
    )
    arrival_date = fields.Date(
        string="Arrival Date",
        required=True,
    )
    trip_location = fields.Char(
        string="Trip Location",
        required=True,
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
        "trip.allowance.form.line",
        "form_id",
        string="Lines",
    )
    signature = fields.Binary(copy=False, store=True)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code("trip.allowance.form")
        return super(TripAllowanceForm, self).create(vals)

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
                "hy_employee_customisation_bhm.mail_activity_trip_allowance",
                user_id=user.id,
            )


class TripAllowanceFormLine(models.Model):
    _name = "trip.allowance.form.line"
    _description = "Trip Allowance Form Line"

    form_id = fields.Many2one(
        "trip.allowance.form",
        string="Form",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )
    no_of_days = fields.Float(
        string="No of Days",
        required=True,
    )
    total_amount = fields.Float(
        string="Total Amount",
        compute="_compute_total_amount",
        store=True,
    )

    @api.depends("amount", "no_of_days")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.amount * record.no_of_days
