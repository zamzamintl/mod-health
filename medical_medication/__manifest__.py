# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).
{
    'name': 'Medical Medication',
    'author': 'LabViv',
    'version': '13.0.0.0.1',
    'website': 'https://labviv.org.ve/',
    'license': 'GPL-3',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_disease',
        'medical_medicament',
    ],
    'summary': 'Introduce medication notion into the medical addons',
    'data': [
        'security/ir.model.access.csv',
        'data/uom_uom.xml',
        'data/medical_medication_dosage.xml',
        'views/medical_medication_dosage_view.xml',
        'views/medical_medication_template_view.xml',
        'views/medical_patient_medication_view.xml',
        'views/medical_patient_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'maintainer': 'Reydi Hernández <rhe@mastercore.net>'
}
