# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2017 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Odoo Medical',
    'summary': 'Adds medical_abstract_entity.',
    'description': 'Medical module ported from OCA/medical-vertical',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'product',
        'base_locale_uom_default',
    ],
    'author': 'LabViv',
    'website': 'https://labviv.org.ve/',
    'license': 'GPL-3',
    'data': [
        'security/medical_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        # 'templates/assets.xml',
        'views/medical_abstract_entity.xml',
        'views/medical_patient.xml',
        'views/res_partner.xml',
        'views/medical_menu.xml',
    ],
    'demo': [
        # 'demo/medical_patient_demo.xml',
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Ángel Ramírez Isea <angel.ramirez.isea@yandex.com>'
}
