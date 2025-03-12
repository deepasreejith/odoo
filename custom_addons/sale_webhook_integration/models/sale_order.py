import requests
import json
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def send_to_webhook(self):
        """Send Sale Order data to Webhook URL."""
        webhook_url = 'https://webhook.site/f63fed36-ae83-4534-9eba-7164d12bf5ea'

        for order in self:
            data = {
                'order_id': order.id,
                'customer': order.partner_id.name,
                'date_order': order.date_order.strftime('%Y-%m-%d %H:%M:%S'),
                'total_amount': order.amount_total,
                'currency': order.currency_id.name,
                'order_lines': [
                    {
                        'product': line.product_id.name,
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'subtotal': line.price_subtotal
                    }
                    for line in order.order_line
                ]
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

            if response.status_code == 200:
                print('Data successfully sent to Webhook.')
            else:
                print(f'Failed to send data. Status code: {response.status_code}')
