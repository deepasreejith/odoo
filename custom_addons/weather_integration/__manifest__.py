{
    'name': 'Weather Integration',
    'summary': 'Build an Odoo Weather App with API Integration',
    'sequence':-200,
    'description': """
        This module create Build an Odoo Weather App with API Integration
    """,
    'author': 'Deepa',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/weather.xml'
    ],
    'installable': True,
    'application': False,
}
