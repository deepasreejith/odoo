from odoo import fields, models, api
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = " estate property details"
    _order = "id asc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")

    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled','Cancelled'),
    ], string='Status', default='new', required=True)

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

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers', ondelete='cascade')
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user.id, ondelete='cascade')
    buyer = fields.Char(string='Buyer')


    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive or zero.'),

    ]

    def unlink(self):
        for property in self:
            if property.status not in ['new', 'cancelled']:
                raise UserError("You cannot delete a property that is not in 'New' or 'Cancelled' status.")
            # If status is 'new' or 'cancelled', continue with deletion
        return super().unlink()
    @api.depends('status')
    def _compute_allow_add_offer(self):
        for property in self:
            if property.status in ['offer_accepted', 'sold', 'cancelled']:
                property.allow_add_offer = False
            else:
                property.allow_add_offer = True

    allow_add_offer = fields.Boolean(string='Allow Add Offer', compute='_compute_allow_add_offer', store=True)
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
            raise UserError("Cannot set cancelled on sold property.")
        else:
            self.status = 'cancelled'

    def action_set_sold(self):

        if self.status == 'cancelled':
            raise UserError("Cannot set sold on cancelled property.")
        else:
            self.status = 'sold'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property_record in self:
            if property_record.selling_price is not None and property_record.expected_price:
                if float_compare(property_record.selling_price, 0,
                                 precision_digits=2) > 0:  # Check if selling price is not zero
                    if float_compare(property_record.selling_price, 0.9 * property_record.expected_price,
                                     precision_digits=2) < 0:
                        raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

    ''' other method
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for property_record in self:
            if property_record.selling_price and property_record.expected_price:
                if property_record.selling_price < (0.9 * property_record.expected_price):
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
    '''