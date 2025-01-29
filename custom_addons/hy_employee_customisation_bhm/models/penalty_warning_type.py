from odoo import models, fields, api, _


class PenaltyWarningType(models.Model):
    _name = "penalty.warning.type"
    _description = "Penalty Warning Type"

    name = fields.Char(string="Name", required=True)
