from odoo import http
from odoo.http import request


class SaleWebhook(http.Controller):
    @http.route('/send_sale_order/<int:order_id>', auth='public', methods=['GET'], csrf=False)
    def send_sale_order(self, order_id, **kwargs):
        """HTTP Route to trigger data sending via URL."""
        order = request.env['sale.order'].sudo().browse(order_id)
        if order:
            order.send_to_webhook()
            return "Data sent to Webhook successfully."
        return "Sale Order not found."
