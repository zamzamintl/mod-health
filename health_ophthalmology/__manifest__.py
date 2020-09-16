# Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical ophthalmology',
    'description': "Medical ophthalmology ported from GNU Health",
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'summary': 'Ophthalmology line to collect results of evaluations',
    'depends': ['medical', 'medical_practitioner'],
    'data': [
        'views/oph_tree.xml',
        'views/oph_form.xml',
        'views/findings_form.xml',
        'views/findings_tree.xml',
        'views/menu.xml',
        'views/health_ophthalmology_report.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>',
}
