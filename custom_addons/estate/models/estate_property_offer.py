from odoo import fields, models, api
from datetime import timedelta
from datetime import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = " estate property offer details"
    _order = "price desc"

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', copy=False,
                              selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ], )

    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date Deadline', compute='compute_date_deadline',
                                inverse='inverse_date_deadline', store=True, readonly=False)

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]

    @api.model
    def create(self, values):
        new_offer = super(EstatePropertyOffer, self).create(values)
        new_offer.property_id.status = 'offer_received'  # Update the status of the related property to 'Offer Received'
        return new_offer

    @api.depends('create_date', 'validity')
    def compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Datetime.from_string(record.create_date).date() + timedelta(
                    days=record.validity)


    def inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Datetime.from_string(record.create_date).date()
                record.validity = (record.date_deadline - create_date).days

    def action_confirm(self):
        for record in self:
            # record.property_id.update_selling_price(record.price)
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id.name
            record.property_id.status = 'offer_accepted'
            record.write({'status': 'accepted'})

    def action_cancel(self):
        for record in self:
            record.write({'status': 'refused'})
            record.property_id.status = 'offer_received'
