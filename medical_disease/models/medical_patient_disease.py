# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models


class MedicalPatientDisease(models.Model):
    _name = 'medical.patient.disease'
    _description = 'Medical Patient Disease'

    @api.depends('short_comment', 'pathology_id', 'pathology_id.name')
    def _compute_name(self):
        self.ensure_one()
        name = self.pathology_id.name
        if self.short_comment:
            name = '%s - %s' % (name, self.short_comment)
        self.name = name

    @api.depends('active')
    def _compute_expire_date(self):
        self.ensure_one()
        if self.active:
            self.expire_date = False
        else:
            self.expire_date = fields.Datetime.now()

    def action_invalidate(self):
        self.ensure_one()
        self.active = False

    def action_revalidate(self):
        self.ensure_one()
        self.active = True

    name = fields.Char(
        compute='_compute_name',
        store=True
    )
    treatment_description = fields.Char()
    expire_date = fields.Datetime(
        compute='_compute_expire_date',
        store=True
    )
    short_comment = fields.Char()
    pathology_id = fields.Many2one(
        comodel_name='medical.pathology',
        string='Pathology', index=True,
        required=True
    )
    physician_id = fields.Many2one(
        comodel_name='medical.practitioner',
        string='Physician', index=True
    )
    patient_id = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient', required=True,
        index=True
    )
    disease_severity = fields.Selection(
        [
            ('1_mi', 'Mild'),
            ('2_mo', 'Moderate'),
            ('3_sv', 'Severe')
        ],
        string='Severity'
    )
    state = fields.Selection(
        [
            ('a', 'Acute'),
            ('c', 'Chronic'),
            ('u', 'Unchanged'),
            ('h', 'Healed'),
            ('i', 'Improving'),
            ('w', 'Worsening'),
        ],
        string='Status of the disease'
    )
    allergy_type = fields.Selection(
        [
            ('da', 'Drug Allergy'),
            ('fa', 'Food Allergy'),
            ('ma', 'Misc Allergy'),
            ('mc', 'Misc Contraindication'),
        ]
    )
    weeks_of_pregnancy = fields.Integer(
        help='Week number of pregnancy when disease contracted',
        string='Pregnancy Week#'
    )
    age = fields.Integer(string='Age when diagnosed')
    active = fields.Boolean(default=True)
    is_infectious = fields.Boolean(string='Infectious Disease')
    is_allergy = fields.Boolean(string='Allergic Disease')
    pregnancy_warning = fields.Boolean()
    is_pregnant = fields.Boolean(string='Pregnancy warning')
    is_on_treatment = fields.Boolean(string='Currently on Treatment')
    treatment_start_date = fields.Date()
    treatment_end_date = fields.Date()
    diagnosed_date = fields.Date(string='Date of Diagnosis')
    healed_date = fields.Date(string='Date of Healing')
    notes = fields.Text()
