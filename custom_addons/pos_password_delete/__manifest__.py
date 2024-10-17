{
    'name': 'POS Password Delete Lines',
    'version': '1.0.0',
    'category': 'Point of Sale',
    'author': 'Deepa',
    'summary': 'Adds a button to delete POS lines with password confirmation.',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_view.xml'
    ],
    'assets':{
        'point_of_sale._assets_pos':[

                'pos_password_delete/static/src/js/button.js',
                'pos_password_delete/static/src/xml/button.xml',

        ]
    },
}