# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'
    medical_center_primary_id = fields.Many2one(
        string='Primary medical center',
        comodel_name='medical.center',
    )
    medical_center_secondary_ids = fields.Many2many(
        string='Secondary medical center',
        comodel_name='medical.center',
    )
