# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MedicalPathologyCategory(models.Model):
    _inherit = 'medical.pathology.category'
    _description = 'Medical Pathology Category'

    notes = fields.Text(translate=True)
    child_ids = fields.One2many(
        string='Children Categories',
        comodel_name='medical.pathology.category',
        inverse_name='parent_id',
        domain="[('code_type_id', '=', code_type_id)]",
    )
    parent_id = fields.Many2one(
        string='Parent Category',
        comodel_name='medical.pathology.category',
        domain="[('code_type_id', '=', code_type_id)]",
        index=True,
    )
    code_type_id = fields.Many2one(
        string='Code Type',
        comodel_name='medical.pathology.code.type',
        index=True,
    )

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for rec in self:
            if not rec._check_recursion():
                raise ValidationError(_(
                    'You are attempting to create a recursive category.'
                ))
