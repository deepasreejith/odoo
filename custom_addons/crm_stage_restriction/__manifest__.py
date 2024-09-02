{
    'name': 'CRM Stage Restriction',
    'version': '1.0',
    'category': 'CRM',
    'summary': 'Add restriction to CRM stages',
    'sequence':-200,
    'description': """
        This module adds a boolean field to the CRM stage model. If this field is true, 
        you cannot move any opportunity to this stage.
    """,
    'author': 'Deepa',
    'depends': ['crm'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crm_stage_view.xml',
    ],
    'installable': True,
    'application': False,
}
