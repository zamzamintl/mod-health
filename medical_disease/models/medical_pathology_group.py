# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPathologyGroup(models.Model):
    _name = 'medical.pathology.group'
    _description = 'Medical Pathology Group'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
    notes = fields.Text(
        string='Notes',
        translate=True
    )
    code = fields.Char(
        required=True,
        help='for example MDG6 code will contain the Millennium Development\
        Goals # 6 diseases : Tuberculosis, Malaria and HIV/AIDS'
    )
    description = fields.Text(
        string='Short Description', required=True, translate=True
    )
