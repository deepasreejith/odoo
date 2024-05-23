{
    'name': 'Hospital Management System',
    'author': 'Deepa',
    'summary': 'Custom hospital management module',
    'depends': ['mail'],
    'sequence': -200,
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
    ],
    'assets': {

    },

    'application': True
}
