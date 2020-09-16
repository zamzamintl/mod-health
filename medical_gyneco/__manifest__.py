# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
{
    'name': 'Medical Gynecology',
    'description': """
        Medical Gyneco Module
        This module includes:
            * Gynecological Information
            * Obstetric information
            * Perinatal Information and monitoring
            * Puerperium
    """,
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'author': 'LabViv',
    'support': 'Julio César Méndez <mendezjcx@thoriumcorp.website>',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'summary': 'GNU Health Gynecology and Obstetrics package',
    'depends': ['medical_physician'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_gyneco_view.xml',
        # data/gnuhealth_commands.xml,
        # security/access_rights.xml,
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>'
}
