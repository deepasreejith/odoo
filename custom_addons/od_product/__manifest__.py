{
    'name': 'Product Template Changes',
    'author': 'Deepa',
    'summary': 'Custom Product Template Changes and create new course module',
    'depends': ['product'],
    'sequence': -200,
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_inherit_view.xml',
        'views/views.xml',
    ],
    'assets': {},
    'application': True
}
