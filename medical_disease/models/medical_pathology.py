# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MedicalPathology(models.Model):
    _name = 'medical.pathology'
    _description = 'Medical Pathology'

    @api.constrains('code')
    def _check_unicity_name(self):
        domain = [
            ('code', '=', self.code),
        ]
        if len(self.search(domain)) > 1:
            raise ValidationError('"code" Should be unique per Pathology')

    name = fields.Char(
        string='Name',
        required=True,
        translate=True
    )
    code = fields.Char(
        string='Code',
        required=True
    )
    notes = fields.Text(
        string='Notes',
        translate=True
    )
    protein = fields.Char(
        string='Protein involved'
    )
    chromosome = fields.Char(
        string='Affected Chromosome'
    )
    gene = fields.Char()
    category_id = fields.Many2one(
        comodel_name='medical.pathology.category',
        string='Category of Pathology',
        index=True
    )
    medical_pathology_group_m2m_ids = fields.Many2many(
        comodel_name='medical.pathology.group',
        column1='pathology_id',
        colmun2='pathology_group_id',
        string='Medical Pathology Groups',
        relation="pathology_id_pathology_group_id_rel"
    )
