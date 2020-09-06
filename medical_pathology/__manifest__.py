# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Pathology',
    'summary': 'Extends Odoo Medical with pathologies (diseases).',
    'author': 'LabViv',
    'version': '13.0.0.0.1',
    'website': 'https://labviv.org.ve/',
    'license': 'GPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'medical',
        'medical_disease',
    ],
    'data': [
        'views/medical_pathology_category_view.xml',
        'views/medical_pathology_view.xml',
        'views/medical_menu.xml',
        'data/medical_pathology_code_type.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/medical_pathology_category_demo.xml',
        'demo/medical_pathology_demo.xml',
    ],
}
