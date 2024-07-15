{
    'name': 'School Management System',
    'author': 'Deepa',
    'summary': 'Custom school management module',
    'depends': [],
    'sequence': -200,
    'data': [
        'data/student.hobby.csv',
        'data/school.profile.csv',
        'data/student.profile.csv',
        'data/school_data.xml',
        'data/student_data.xml',
        'data/no_update_sample.xml',
        'security/ir.model.access.csv',
        'wizard/student_fee_update_wizard_view.xml',
        'views/school_view.xml',
        'views/student_view.xml',
        'views/menu.xml',
        'data/delete_data.xml',
        'reports/student_report_template.xml',
        'reports/inherit_qweb_template.xml',
    ],
    'demo': [
        'demo/demo_school_data.xml',
    ],

    'assets': {

    },

    'application': True
}
