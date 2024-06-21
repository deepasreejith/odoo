from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(string='Instructor',default=False)
    session_id = fields.Many2many('od_product.session',string='Attended sessions')
