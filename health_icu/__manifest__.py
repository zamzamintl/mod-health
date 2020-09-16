# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': "gnuhealth_icu",
    'summary': "GNU Health package for Intensive Care settings",
    'description': "GNU Health package for Intensive Care settings",
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'depends': [
        'base',
        'medical',
        # 'health_inpatient'
        # health_nursing
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/gnuhealth_icu_apache2_form.xml',
        'views/gnuhealth_icu_apache2_tree.xml',
        'views/gnuhealth_icu_chest_drainage_form.xml',
        'views/gnuhealth_icu_chest_drainage_tree.xml',
        'views/gnuhealth_icu_glasgow_form.xml',
        'views/gnuhealth_icu_glasgow_tree.xml',
        'views/gnuhealth_icu_ventilation_form.xml',
        'views/gnuhealth_icu_ventilation_tree.xml',
        'views/medical_patient.xml',
        # 'views/gnuhealth_patient_icu_rounding.xml',
        'views/health_icu_view.xml'
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>'
}
