# Copyright 2017 LasLabs Inc.
# Copyright 2017 Creu Blanca.
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class MedicalSpecialty(models.Model):
    _name = 'medical.specialty'
    _description = 'Medical Specialty'
    _sql_constraints = [
        ('code_uniq', 'UNIQUE(code)', 'Code must be unique!'),
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]

    code = fields.Char(
        string='Code',
        help='Speciality code',
        size=256,
        required=True,
    )
    name = fields.Char(
        string='Name',
        help='Name of the specialty',
        size=256,
        required=True,
    )
    category = fields.Selection(
        [
            ('clinical', 'Clinical specialties'),
            ('surgical', 'Surgical specialties'),
            ('medical', 'Medical-surgical specialties'),
            ('diagnostic', 'Laboratory or diagnostic specialties'),
        ],
        'Category of specialty'
    )
    # This is referenced in
    # https://es.wikipedia.org/wiki/Especialidades_médicas#Especialidades_clínicas
