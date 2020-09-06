#
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
#
{
    'name': 'Odoo Medical Extras',
    'summary': 'Extends medical_abstract_entity.',
    'description': 'Medical module ported from OCA/medical-vertical',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'base_locale_uom_default',
        'medical'
    ],
    'author': "LabViv",
    'website': "https://www.labviv.org.ve",
    'maintainer': 'Julio César Méndez <mendezjcx@tutanota.com>',
    'license': 'GPL-3',
    'data': [
        'security/ir.model.access.csv',
        # 'views/template.xml',
        'views/views.xml',
        'data/medical_extras_sequence.xml',
    ],
    'demo': [
        # 'demo/medical_patient_demo.xml',
    ],
    'installable': True,
    'application': False,
}
