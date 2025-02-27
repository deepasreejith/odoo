from odoo import models, fields, api
from num2words import num2words


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_words = fields.Char(string="Amount in Words", compute="_compute_amount_words")

    @api.depends('amount_total')
    def _compute_amount_words(self):
        for order in self:
            order.amount_words = num2words(order.amount_total, to='currency', lang='en')