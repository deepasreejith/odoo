{
    'name': 'Hospital Management System',
    'author': 'Deepa',
    'summary': 'Custom hospital management module',
    'depends': ['mail','product','account', 'web','base'],
    'sequence': -200,
    'data': [
        # 'views/templates.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence.xml',
        'data/mail_template_data.xml',
        'wizard/cancel_appointment_view.xml',

        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/operation_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',
        'views/invoice_inheritance_view.xml',
        'report/patient_card_template.xml',
        'report/report.xml',
        # 'report/sale_report_inherit.xml',

    ],
    'assets': {

    },

    'application': True
}
