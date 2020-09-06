# Copyright 2008-2020 Luis Falcon <falcon@gnuhealth.org>.
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Health Vaccination',
    'summary': 'Vaccination records',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_center',
        'medical_medicament',
    ],
    'Author': 'LabViv',
    'website': "https://www.labviv.org.ve",
    'description': "Vaccination records",
    'license': 'GPL-3',
    'data': [
        'views/product_product_view.xml',
        'views/medical_patient_view.xml',
        'views/medical_vaccination_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'maintainer': 'Reydi Hernández <rhe@mastercore.net>'
}
