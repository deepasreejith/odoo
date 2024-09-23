from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        """
        Override the _action_confirm method to block automatic delivery creation
        by skipping the call to _action_launch_stock_rule.
        """
        print("test")
        return


    def action_create_delivery(self):
        for order in self:
            order.order_line._action_launch_stock_rule()
