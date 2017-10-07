# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        open academy""",

    'description': """
        sherman's open academy
    """,

    'author': "sherman",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report','board'],

    # always loaded
    'data': [
        'views/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/openacademy.xml',
        'views/sessions.xml',
        'views/partner.xml',
        'views/wizard.xml',
        'views/session_workflow.xml',
        'views/session_board.xml',
        'views/reports.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': 'True'
}
