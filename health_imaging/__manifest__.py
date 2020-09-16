# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Imaging',
    'description': """Medical Diagnostic Imaging management package
        - Imaging types and tests.
        - Imaging test requests and results.""",
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'summary': 'Diagnostic Imaging management package',
    'depends': ['medical'],
    'data': [
        'security/ir.model.access.csv',
        'views/imaging_test_form.xml',
        'views/imaging_test_request_form.xml',
        'views/imaging_test_request_tree.xml',
        'views/imaging_test_result_form.xml',
        'views/imaging_test_tree.xml',
        'views/imaging_test_result_tree.xml',
        'views/imaging_test_type_form.xml',
        'views/imaging_test_type_tree.xml',
        # 'views/patient_imaging_test_request_start_form.xml',
        'views/health_imaging_view.xml',
        'data/health_imaging_sequences.xml',
        'data/imaging_data.xml',
    ],
    'installable': True,
    'application': True,
    'maintainer': 'Julio César Méndez <mendezjcx@thoriumcorp.website>',
}
