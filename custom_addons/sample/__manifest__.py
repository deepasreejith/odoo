{
    'name':'Sample module',
    'author': 'Deepa',
    'summary': 'Custom Sample module fot inheritance',
    'depends': ['base','sale','mail'],
    'sequence': -200,
    'data': [
        'views/sale_order_view.xml',
        'views/res_partner_inherit_view.xml',
    ],
    'assets': {},
    'application': True
}