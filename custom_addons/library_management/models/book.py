from odoo import models, fields

class Book(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title', required=True)
    author_id = fields.Many2one('library.author', string='Author')
    isbn = fields.Char(string='ISBN')
    published_date = fields.Date(string='Published Date')
