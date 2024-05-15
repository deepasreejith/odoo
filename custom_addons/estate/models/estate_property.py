from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = " estate property details"


    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    status = fields.Char(string="Status", default="New")
    date_availability = fields.Date(string="Date Availability", default=fields.Date.today())
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms", default=4)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')], )
    total_area = fields.Float(string='Total Area(sqm)', readonly=True, compute="_compute_total_area")
    best_price = fields.Float(string='Best Offer', compute='compute_best_offer')

    property_type = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user.id)
    buyer = fields.Char(string='Buyer')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_cancel(self):
        if self.status == 'sold':
            raise UserError("Cannot set sold on cancelled property.")
        else:
            self.status = 'cancelled'

    def action_set_sold(self):
        if self.status == 'cancelled':
            raise UserError("Cannot set cancelled on sold property.")
        else:
            self.status = 'sold'


    '''def update_selling_price(self, price):
        for record in self:
            record.selling_price = price'''