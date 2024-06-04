{
    'name': 'Hospital Management System',
    'author': 'Deepa',
    'summary': 'Custom hospital management module',
    'depends': ['mail','product'],
    'sequence': -200,
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/operation_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {

    },

    'application': True
}
