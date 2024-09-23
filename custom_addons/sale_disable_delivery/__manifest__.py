{
    'name': 'Sale Disable Delivery',
    'author': 'Deepa',
    'description': 'This module Disable delivery create while sale order and add a button to manually create delivery',
    'depends': ['sale_management', 'stock'],
    'sequence':-200,
    'data': [
            'views/sale_order_views.xml',
    ],
    'assets':{

    },

    'application':True
}