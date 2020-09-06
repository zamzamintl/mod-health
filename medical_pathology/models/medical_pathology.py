# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MedicalPathology(models.Model):
    _inherit = 'medical.pathology'
    _description = 'Medical Pathology'

    code_type_id = fields.Many2one(
        string='Code Type',
        comodel_name='medical.pathology.code.type',
        index=True,
    )
    category_id = fields.Many2one(
        string='Category of Pathology',
        comodel_name='medical.pathology.category',
        domain="[('code_type_id', '=', code_type_id)]",
        index=True,
    )
    child_ids = fields.One2many(
        string='Children Pathologies',
        comodel_name='medical.pathology',
        inverse_name='parent_id',
        domain="[('code_type_id', '=', code_type_id)]",
    )
    parent_id = fields.Many2one(
        string='Parent Pathology',
        comodel_name='medical.pathology',
        domain="[('code_type_id', '=', code_type_id)]",
        index=True,
    )

    _sql_constraints = [
        ('code_and_type_uniq',
         'UNIQUE(code, code_type_id)',
         'Pathology codes must be unique per code type.'),
    ]

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for rec in self:
            if not rec._check_recursion():
                raise ValidationError(_(
                    'You are attempting to create a recursive pathology.'
                ))
