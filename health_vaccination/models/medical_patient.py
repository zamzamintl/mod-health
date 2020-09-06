# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    vaccination_ids = fields.One2many(
        comodel_name='medical.vaccination',
        inverse_name='patient_id',
        string='Vaccinations',
        readonly=True
    )
