# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Health Family',
    'summary': 'Familia',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_pathology',
        'housing',
        'medical_insurance'
    ],
    'author': 'LabViv',
    'website': "https://git.labviv.org.ve/",
    'description': 'Información detallada de la Familia y sus miembros',
    'license': 'GPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/ethnic_groups.xml',
        'data/occupations.xml',
        'views/health_family_member.xml',
        'views/health_family.xml',
        'views/family_menu.xml',
        # 'views/alternative_identification.xml',
        # 'views/birth_certificate.xml',
        # 'views/death_certificate.xml',
        # 'views/contact_mechanism.xml',
        # 'views/ethnicity.xml',
        # 'views/family_address.xml',
        # 'views/insurane_family.xml',
        # 'views/insurane_plan_family.xml',
        # 'views/occupation.xml',
        # 'views/person_name.xml',
        # 'views/res_partner.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Kaylenis Mardach <kaykmm@yandex.com>'
}
