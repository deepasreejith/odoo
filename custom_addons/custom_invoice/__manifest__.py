{
    'name': 'Custom Invoice Remarks',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add manager and director remarks to customer invoices',
    'description': """
        This module adds two new fields, Manager Remarks and Director Remarks,
        to the customer invoice form in Odoo.
    """,
    'sequence':-200,
    'author': 'Deepa',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/invoice_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
