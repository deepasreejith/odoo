from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_visit_form_count = fields.Integer(
        string="Employee Visit Form Count",
        compute="_compute_employee_visit_form_count",
    )
    employee_penalty_form_count = fields.Integer(
        string="Employee Penalty Form Count",
        compute="_compute_employee_penalty_form_count",
    )
    employee_task_ids = fields.One2many("employee.task", "employee_id", string="Tasks")

    def _compute_employee_penalty_form_count(self):
        for rec in self:
            rec.employee_penalty_form_count = self.env[
                "employee.penalty.form"
            ].search_count([("employee_id", "=", rec.id)])

    def action_view_penalty_form(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "hy_employee_customisation_bhm.employee_penalty_form_action"
        )
        action["context"] = {
            "default_employee_id": self.id,
            "default_company_id": self.company_id.id,
        }
        action["domain"] = [("employee_id", "=", self.id)]
        if self.employee_penalty_form_count == 1:
            penalty_form_id = self.env["employee.penalty.form"].search(
                [("employee_id", "=", self.id)]
            )
            penalty_form_ids = sum([penalty_form_id.id])
            res = self.env.ref(
                "hy_employee_customisation_bhm.employee_penalty_form_view_form", False
            )
            action["views"] = [(res and res.id or False, "form")]
            action["res_id"] = penalty_form_ids or False
        return action

    def _compute_employee_visit_form_count(self):
        for rec in self:
            rec.employee_visit_form_count = self.env[
                "employee.visit.form"
            ].search_count([("employee_id", "=", rec.id)])

    def action_view_visit_form(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "hy_employee_customisation_bhm.employee_visit_form_action"
        )
        action["context"] = {
            "default_employee_id": self.id,
            "default_company_id": self.company_id.id,
        }
        action["domain"] = [("employee_id", "=", self.id)]
        if self.employee_visit_form_count == 1:
            visit_form_id = self.env["employee.visit.form"].search(
                [("employee_id", "=", self.id)]
            )
            visit_form_ids = sum([visit_form_id.id])
            res = self.env.ref(
                "hy_employee_customisation_bhm.employee_visit_form_view_form", False
            )
            action["views"] = [(res and res.id or False, "form")]
            action["res_id"] = visit_form_ids or False
        return action
