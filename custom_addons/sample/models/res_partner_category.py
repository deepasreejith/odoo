from odoo import fields,models,api

class ResPartnerCategory(models.Model):

    _name = 'res.partner.category'
    _inherit = ['res.partner.category','mail.thread']





