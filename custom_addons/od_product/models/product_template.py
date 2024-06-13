from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    processor = fields.Char(string='Processor')