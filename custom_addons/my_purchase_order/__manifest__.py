{
    'name': 'My Purchase Order',
    'author': 'Deepa',
    'summary': 'Custom Purchase Order Template',
    'depends': ['base','purchase'],
    'sequence':-100,
    'data': [
        'reports/purchase_report.xml',
        'reports/purchase_report_template.xml',
        #'reports/purchase_inherit_template.xml'
    ],
    'assets':{
        'web.report_assets_common':[
            'my_purchase_order/static/src/scss/**/*',
        ]
    },

    'application':True
}