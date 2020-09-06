# Copyright 2017 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html)

from odoo import fields, models


class MedicalProcedure(models.Model):
    _name = 'medical.procedure'
    _description = 'Medical Procedure'

    name = fields.Char(
        required=True,
        help='Name of procedure, such as "Behavioral therapy"',
    )
    code = fields.Char(
        help='Short name or code for procedure',
        required=True,
    )
    description = fields.Text()
    active = fields.Boolean(default=True)
