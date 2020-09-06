# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


{
	'name': 'Health Surgery',
	'summary': 'Cirugía y chequeos quirúrgicos',
	'version': '13.0.0.0.1',
	'category': 'Medical',
	'depends': [
		'medical',
		'medical_center',
		'medical_physician',
		'medical_practitioner',
		'medical_disease',
		'medical_pathology',
		],
	'author': 'LabViv',
	'website': 'http://www.labviv.org.ve',
	'description': """
		- Chequeo pre-quirúrgico.
		- Procedimientos.
		- Información de quirófanos.
		- Historial quirúrgico del paciente.
		""",
	'license':  'GPL-3',
	'data': [
		'security/ir.model.access.csv',
		'data/gnuhealth_commands.xml',
		'data/health_surgery_sequence.xml',
		'views/surgery.xml',
		'views/surgery_operation.xml',
		'views/surgery_procedure.xml',
		'views/surgery_rcri.xml',
		'views/surgery_supply.xml',
		'views/surgery_team.xml',
		#'views/templates.xml',
		#'views/views.xml',
	],
	'demo': [],
	'instalable': True,
	'application': True,
	'maintainer': 'Kaylenis Mardach <kaykmm@yandex.com>'
}
