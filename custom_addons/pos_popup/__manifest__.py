{
    'name': 'POS Popup',
    'summary': 'Add a custom button to the POS module',
    'description': 'This module adds a custom button to the Point of Sale interface using OWL components.',
    'depends': ['point_of_sale'],
    'sequence':-200,
    'data': [

    ],
    'assets':{
        'point_of_sale._assets_pos':[
                'pos_popup/static/src/js/button.js',
                'pos_popup/static/src/xml/button.xml',
                'pos_popup/static/src/js/popup_button.js',
                'pos_popup/static/src/xml/popup_button.xml',

        ]
    },

    'application':True
}