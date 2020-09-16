# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Insurance',
    'summary': 'Medical Insurance.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
    ],
    'author': 'LabViv',
    'website': "https://git.labviv.org.ve/",
    'license': 'GPL-3',
    'description': 'Medical_Insurance module ported from OCA/medical-vertical',
    'data': [
        'views/medical_insurance_company_view.xml',
        'views/medical_insurance_template_view.xml',
        'views/medical_insurance_plan_view.xml',
        'views/medical_patient_view.xml',
        'security/ir.model.access.csv',
        'views/medical_menu.xml',
    ],
    "demo": [
        # "demo/product_product_demo.xml",
        # "demo/medical_insurance_company_demo.xml",
        # "demo/medical_insurance_template_demo.xml",
        # "demo/medical_insurance_plan_demo.xml",
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Kaylenis Mardach <kaykmm@yandex.com>'
}
