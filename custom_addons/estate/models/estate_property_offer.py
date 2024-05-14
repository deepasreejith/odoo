from odoo import fields, models,api
from datetime import timedelta
from datetime import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = " estate property offer details"

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    price = fields.Float(string='Price')
    status = fields.Selection(string='Status',copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'),],)

    validity = fields.Integer(string='Validity',default=7)
    date_deadline = fields.Date(string='Date Deadline',compute='compute_date_deadline', inverse='inverse_date_deadline', store=True, readonly=False)

    @api.depends('create_date','validity')
    def compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)
    def inverse_date_deadline(self):
            for record in self:
                if record.date_deadline and record.create_date:
                    create_date = record.create_date.date()
                    record.validity = (record.date_deadline - create_date).days