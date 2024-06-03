from odoo import models, fields, api
from datetime import datetime

class PurchaseConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    notification_before = fields.Integer(string="Notification Before (Days)",config_parameter='purchase_order_notification.notification_before')

class MyPurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    @api.model
    def check_notification(self):
        notification_before_days = int(self.env['ir.config_parameter'].sudo().get_param('purchase_order_notification.notification_before', default=0))
        print(notification_before_days)
        print(fields.Date.today())
        today = datetime.combine(fields.Date.today(), datetime.min.time())  # Convert to datetime
        print(today)
        orders = self.search([('state', '=', 'purchase'), ('date_planned', '>=', today)])
        for order in orders:
            days_until_arrival = (order.date_planned - today).days
            if days_until_arrival == notification_before_days:
                order.create_activity()

    def create_activity(self):
        for order in self:
            user_id = order.user_id.id
            activity = self.env['mail.activity'].create({
                'res_id': order.id,
                'res_model_id': self.env.ref('purchase.model_purchase_order').id,
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Reminder for expected arrival',
                'note': f'your order is reached with in days',
                'user_id': user_id,  # Assign the activity to the user
            })
