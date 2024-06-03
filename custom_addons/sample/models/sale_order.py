from odoo import fields,models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirm_user_id = fields.Many2one('res.users',string='Confirm User')
    
    def action_cancel(self):
        print("success.....")
        # super(SaleOrder,self).action_cancel()
