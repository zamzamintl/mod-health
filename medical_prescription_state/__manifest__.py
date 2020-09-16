# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Prescription Order States',
    'summary': 'This module introduce the prescription/prescription state ',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical_prescription',
    ],
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'data': [
        'views/medical_prescription_order_state_view.xml',
        'views/prescription_order_view.xml',
        'views/medical_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
