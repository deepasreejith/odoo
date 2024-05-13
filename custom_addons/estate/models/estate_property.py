from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = " estate property details"

    name = fields.Char(string="Name",required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="PostCode")
    date_availability = fields.Date(string="Date Availability",default=fields.Date.today())
    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms",default=4)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],)

    property_type = fields.Many2one('estate.property.type',string='Property Type')



