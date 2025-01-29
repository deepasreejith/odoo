from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = "res.users"

    require_signature = fields.Binary(string="Signature")
