{
    'name': 'Dynamic Snippet',
    'summary': 'Create Dynamic snippet',
    'sequence':-200,
    'description': """
        This module create my own snippets that will show images of last created three products
    """,
    'author': 'Deepa',
    'depends': ['website'],
    'data': [
        'views/snippet.xml',
        'views/dynamic_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'dynamic_snippet/static/src/js/dynamic_snippet.js',
        ],
    },

    'installable': True,
    'application': True,
}
