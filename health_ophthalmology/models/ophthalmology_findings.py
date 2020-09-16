# Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class OphthalmologyFindings(models.Model):
    _name = 'ophthalmology.findings'
    _description = 'OphthalmologyFindings'

    name = fields.Many2one(
        'ophthalmology.evaluation',
        'Evaluation',
        readonly=True
    )
    eye_structure = fields.Selection(
        [
            ('lid', 'Lid'),
            ('ncs', 'Naso-lacrimal system'),
            ('conjuctiva', 'Conjunctiva'),
            ('cornea', 'Cornea'),
            ('anterior_chamber', 'Anterior Chamber'),
            ('iris', 'Iris'),
            ('pupil', 'Pupil'),
            ('lens', 'Lens'),
            ('vitreous', 'Vitreous'),
            ('fundus_disc', 'Fundus Disc'),
            ('macula', 'Macula'),
            ('fundus_background', 'Fundus background'),
            ('fundus_vessels', 'Fundus vessels'),
            ('other', 'Other'),
        ],
        'Structure',
        help="Affected eye structure",
        sort=False
    )
    affected_eye = fields.Selection(
        [
            ("right", "right"),
            ("left", "left"),
            ("both", "both"),
        ],
        'Eye',
        help="Affected eye",
        sort=False
    )
    finding = fields.Char('Finding')
