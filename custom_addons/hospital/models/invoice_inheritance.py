from odoo import fields,models,api


class InvoiceInheritance(models.Model):

    _inherit = 'account.move.line'


    line_num = fields.Integer(string='Line Number')
