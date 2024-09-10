{
    'name': 'Custom POS',
    'author': 'Deepa',
    'summary': 'Add a custom button to the POS module',
    'description': 'This module adds a custom button to the Point of Sale interface using OWL components.',
    'depends': ['point_of_sale'],
    'sequence':-200,
    'data': [

    ],
    'assets':{
            'point_of_sale._assets_pos':[
                'custom_pos/static/src/js/sample_button.js',
                'custom_pos/static/src/js/sample_popup_button.js',
                'custom_pos/static/src/xml/sample_button.xml',
                'custom_pos/static/src/xml/sample_popup_button.xml',
            ]
    },

    'application':True
}