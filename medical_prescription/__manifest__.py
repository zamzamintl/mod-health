# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>).
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Prescription',
    'description': 'Medical Prescriptions ported from OCA/medical-vertical',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_medicament',
        'medical_medication',
    ],
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'summary': 'This module introduces prescription/prescription line '
    'into the medical addons.',
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/medical_prescription_order_view.xml',
        'views/medical_prescription_order_line_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'maintainer': 'Julio César Mendez <mendezjcx@tutanota.com>'
}
