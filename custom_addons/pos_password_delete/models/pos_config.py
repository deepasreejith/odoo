from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    delete_order_password = fields.Char(string="Delete Order Password")

