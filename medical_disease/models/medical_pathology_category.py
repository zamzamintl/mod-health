# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MedicalPathologyCategory(models.Model):
    _name = 'medical.pathology.category'
    _description = 'Medical Pathology Category'

    @api.constrains('parent_id')
    def _check_recursion_parent_id(self):
        if not self._check_recursion():
            raise ValidationError('Error! You cannot create a recursive zone.')

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
    child_ids = fields.One2many(
        comodel_name='medical.pathology.category',
        inverse_name='parent_id',
        string='Children Categories'
    )
    parent_id = fields.Many2one(
        comodel_name='medical.pathology.category',
        string='Parent Category',
        index=True
    )
