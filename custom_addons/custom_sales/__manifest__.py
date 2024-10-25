{
    'name': 'Custom Sales',
    'author': 'Deepa',
    'summary': 'Add a custom button to the Sales module and add actions',
    'description': 'This module adds a custom button to the Sales order interface and when it click a kanban view open with details of thats order attachments.',
    'depends': ['mail','sale'],
    'sequence':-200,
    'data': [
        'views/attachment_kanban_view.xml',
    ],
    'assets':{
        'web.assets_backend': [
            'custom_sales/static/src/xml/chatter_inherit.xml',
            'custom_sales/static/src/js/chatter_patch.js',
        ],
    },

    'application':True
}