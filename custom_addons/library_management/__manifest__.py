{
    'name': 'Library Management',
    'version': '1.0',
    'author': 'Deepa',
    'category': 'Library',
    'summary': 'Manage books and authors',
    'sequence': -200,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/author_view.xml',
        'report/books_detail_template.xml',
        'report/report.xml'
    ],
    'installable': True,
    'application': True,
}
