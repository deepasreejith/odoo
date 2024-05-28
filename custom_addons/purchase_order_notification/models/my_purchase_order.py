from odoo import models, fields, api

class MyPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    notification_before = fields.Integer(string="Notification Before (Days)")
    test = fields.Char(string='test')