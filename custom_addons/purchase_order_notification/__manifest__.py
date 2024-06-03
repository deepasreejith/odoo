{
    'name':'Purchasr Order Notification',
    'author': 'Deepa',
    'summary': 'Custom Purchase Notification module',
    'depends': ['base','purchase'],
    'sequence': -200,
    'data': [
        'data/cron.xml',
        'views/purchase_config_settings_view.xml',
    ],
    'assets': {},
    'application': True
}