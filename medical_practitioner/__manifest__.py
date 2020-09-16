# Copyright 2017 LasLabs Inc.
# Copyright 2017 Creu Blanca.
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical_Practitioner',
    'version': '13.0.0.0.1',
    'summary': 'Registro de profesionales de la salud',
    'author': 'LabViv',
    'description':
        'Medical_Practitioner module ported from OCA/medical-vertical',
    'website': "https://git.labviv.org.ve/",
    'license': 'GPL-3',
    'category': 'Medical',
    'depends': ['medical'],
    'data': [
        'data/ir_sequence.xml',
        'data/medical_role.xml',
        'data/medical_specialty.xml',
        'security/ir.model.access.csv',
        'views/medical_practitioner.xml',
        'views/medical_role.xml',
        'views/medical_menu.xml',
        'views/medical_specialty.xml',
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Kaylenis Mardach <kaykmm@yandex.com>'
}
