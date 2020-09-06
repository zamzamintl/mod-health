# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, api
from odoo.models import MAGIC_COLUMNS


class AbstractMedicalMedication(models.AbstractModel):
    _name = 'abstract.medical.medication'
    _description = 'Abstract Medical Medication'

    @api.onchange('medication_template_id')
    def onchange_template_id(self):
        if self.medication_template_id:
            values = self.medication_template_id.read()[0]
            for k in values.keys():
                if k not in MAGIC_COLUMNS:
                    setattr(self, k, getattr(self.medication_template_id, k))
