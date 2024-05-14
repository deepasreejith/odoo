from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = " estate property offer details"

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    price = fields.Float(string='Price')
    status = fields.Selection(string='Status',copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'),],)
