# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    "name": "Medical Centers",
    "summary": "Adds a concept of Medical Centers to Patients.",
    'version': '13.0.0.0.1',
    "category": "Medical",
    'website': 'https://labviv.org.ve/',
    "author": "LabViv",
    "license": "GPL-3",
    'description': "Medical_Center module ported from OCA/medical-vertical.",
    "depends": [
        "medical",
        "medical_practitioner",
    ],
    "data": [
        "views/medical_center.xml",
        "views/medical_patient.xml",
        "views/medical_menu.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        # "demo/medical_center.xml",
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Giovanny Avila <Giovany Avila <gjavilae@gmail.com>'
}
