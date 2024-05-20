from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property','salesperson',string='Properties',domain=[('status', 'in', ['new', 'offer_received','offer_accepted'])],
        help="Properties assigned to this user as salesperson.",readonly=True)

    print(property_ids)