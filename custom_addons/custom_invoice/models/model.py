from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    manager_remarks = fields.Text(string='Manager Remarks')
    director_remarks = fields.Text(string='Director Remarks')
    manager_remarks_readonly = fields.Boolean(compute='_compute_manager_remarks_readonly', store=False)
    director_remarks_readonly = fields.Boolean(compute='_compute_director_remarks_readonly', store=False)

    @api.depends('state')
    def _compute_manager_remarks_readonly(self):
        for record in self:
            record.manager_remarks_readonly = record.state != 'draft' or not self.env.user.has_group(
                'custom_invoice.group_sales_custom_manager')

    @api.depends('state')
    def _compute_director_remarks_readonly(self):
        for record in self:
            record.director_remarks_readonly = record.state != 'draft' or not self.env.user.has_group(
                'custom_invoice.group_sales_custom_director')

    def action_post(self):
        # Check if Manager Remarks and Director Remarks have values before posting
        for record in self:
            if not record.manager_remarks:
                raise ValidationError("You cannot post the invoice until Manager Remarks are filled.")
            if not record.director_remarks:
                raise ValidationError("You cannot post the invoice until Director Remarks are filled.")
        return super(AccountMove, self).action_post()
