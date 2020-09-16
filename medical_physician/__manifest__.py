# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Physician',
    'author': 'LabViv',
    'version': '13.0.0.0.1',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    "category": "Medical",
    'depends': ['medical_center'],
    "data": [
        'views/medical_physician_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
        'wizard/medical_physician_unavailable_view.xml',
        'data/ir_sequence_data.xml',
    ],
    'demo': ['demo/medical_physician.xml'],
    'installable': True,
    'maintainer': 'Reydi Hernández <rhe@mastercore.net>'
}
