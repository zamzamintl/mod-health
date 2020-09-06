# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "DGDS Viviendas",
    'summary': "Unidad de vivienda para el SDGDS",
    'description': "Unidad de vivienda para SDGDS. Basado en GNUHealth.",
    'author':  "LabViv",
    'website': 'https://labviv.org.ve/',
    'installable': True,
    'application': True,
    'category': 'Medical',
    'version': '13.0.0.0.1',
    'depends': ['medical_center'],
    'data': [
        'security/ir.model.access.csv',
        'views/housing.xml',
        'views/menu.xml',
        'views/res_partner.xml',
    ],
    'demo': [],
    'maintainer': 'Giovany Avila <gjavilae@gmail.com'
}
