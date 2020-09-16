# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'fleet_vehicle_type',
    'description': 'Allows many different types of vehicles (not just cars).',
    'version': '13.0.0.0.1',
    'category': 'SisteMASo',
    'depends': ['fleet'],
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'data': [
        'data/fleet_vehicle_type_data.xml',
        'security/ir.model.access.csv',
        'views/fleet_vehicle_type_v.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Ángel Ramírez Isea <angel.ramirez.isea@yandex.com>'
}
