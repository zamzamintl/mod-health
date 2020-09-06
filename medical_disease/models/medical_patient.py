# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    def action_invalidate(self):
        super(MedicalPatient, self).action_invalidate()
        self.disease_ids.action_invalidate()

    def compute_count_disease_ids(self):
        self.count_disease_ids = len(self.disease_ids)

    disease_ids = fields.One2many(
        comodel_name='medical.patient.disease',
        inverse_name='patient_id',
        string='Diseases'
    )
    count_disease_ids = fields.Integer(
        compute='compute_count_disease_ids',
        string='NB. Disease'
    )
