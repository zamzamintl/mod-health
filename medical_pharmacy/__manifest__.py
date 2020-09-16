# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Pharmacy',
    'summary': 'Adds a pharmacy namespace on partners.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
    ],
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'data': [
        'views/medical_pharmacy_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'maintainer': 'Julio César Mendez <mendezjcx@tutanota.com>'
}
