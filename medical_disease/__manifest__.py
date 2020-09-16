# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2017 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Disease',
    'description': 'Medical Disease module ported from OCA/medical-vertical',
    'author': 'LabViv',
    'version': '13.0.0.0.1',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'category': 'Medical',
    'depends': ['medical_practitioner'],
    'summary': 'Introduce disease notion into the medical category',
    'data': [
        'security/ir.model.access.csv',
        # 'views/medical_pathology_view.xml',
        # 'views/medical_pathology_category_view.xml',
        'views/medical_pathology_group_view.xml',
        'views/medical_patient_disease_view.xml',
        'views/medical_patient_view.xml',
        'views/medical_disease_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'maintainer': 'Reydi Hernández <rhe@mastercore.net>'
}
