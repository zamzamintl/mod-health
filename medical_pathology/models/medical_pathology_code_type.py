# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class MedicalPathologyCodeType(models.Model):
    _name = 'medical.pathology.code.type'
    _description = 'Medical Pathology Code Type'

    name = fields.Char(required=True)
