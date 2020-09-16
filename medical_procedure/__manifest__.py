# Copyright 2017 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html)

{
    'name': 'Medical Procedures',
    'summary': 'Adds notion of medical procedure used elsewhere in medical',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'application': True,
    'installable': True,
    'depends': ['medical'],
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/medical_procedure.xml',
    ],
    'demo': ['demo/medical_procedure.xml'],
    'maintainer': 'Julio César Mendez <mendezjcx@tutanota.com>'
}
