{
    'name': 'Real Estate',
    'author': 'Deepa',
    'summary': 'Custom real estate module',
    'depends': [],
    'sequence':-200,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
    ],
    'assets':{

    },

    'application':True
}