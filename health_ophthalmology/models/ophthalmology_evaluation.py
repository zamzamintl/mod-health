# Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
STATES = {'done': [('readonly', True)]}


class OphthalmologyEvaluation(models.Model):
    _name = 'ophthalmology.evaluation'
    _description = 'Ophthalmology Evaluation'

    @api.model
    def default_health_professional(self):
        loging_user = self.env.user
        health_professional = loging_user.partner_id
        return health_professional

    name = fields.Char(string="Name")
    patient = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        required=True
    )
    visit_date = fields.Datetime(
        string='Date',
        help="Date of Consultation",
        default=fields.Datetime.now
    )
    health_professional = fields.Many2one(
        comodel_name='medical.practitioner',
        string='Health Professional',
        readonly=True,
        help="Health professional / Ophthalmologist / OptoMetrist",
        default=default_health_professional
     )
    snellen_chart = [
        ('6_6', '6/6'),
        ('6_9', '6/9'),
        ('6_12', '6/12'),
        ('6_18', '6/18'),
        ('6_24', '6/24'),
        ('6_36', '6/36'),
        ('6_60', '6/60'),
        ('5_60', '5/60'),
        ('4_60', '4/60'),
        ('3_60', '3/60'),
        ('2_60', '2/60'),
        ('1_60', '1/60'),
        ('1_meter_fc', '1 Meter FC'),
        ('1_2_meter_fc', '1/2 Meter FC'),
        ('hmfc', 'HMCF'),
        ('p_l', 'P/L'),
    ]
    near_vision_chart = [
        ('N6', 'N6'),
        ('N8', 'N8'),
        ('N12', 'N12'),
        ('N18', 'N18'),
        ('N24', 'N24'),
        ('N36', 'N36'),
        ('N60', 'N60'),
    ]
    rdva = fields.Selection(
        snellen_chart,
        'RDVA',
        help="Right Eye Vision of Patient without aid",
        sort=False,
        states=STATES
    )
    ldva = fields.Selection(
        snellen_chart,
        'LDVA',
        help="Left Eye Vision of Patient without aid",
        sort=False,
        states=STATES
    )
    rdva_pinhole = fields.Selection(
        snellen_chart,
        'RDVA',
        help="Right Eye Vision Using Pin Hole",
        sort=False,
        states=STATES
    )
    ldva_pinhole = fields.Selection(
        snellen_chart,
        'LDVA',
        help="Left Eye Vision Using Pin Hole",
        sort=False,
        states=STATES
    )
    rdva_aid = fields.Selection(
        snellen_chart,
        'RDVA AID',
        help="Vision with glasses or contact lens",
        sort=False,
        states=STATES
    )
    ldva_aid = fields.Selection(
        snellen_chart,
        'LDVA AID',
        help="Vision with glasses or contact lens",
        sort=False,
        states=STATES
    )
    rspherical = fields.Float('SPH', help='Right Eye Spherical', states=STATES)
    lspherical = fields.Float('SPH', help='Left Eye Spherical', states=STATES)
    rcylinder = fields.Float('CYL', help='Right Eye Cylinder', states=STATES)
    lcylinder = fields.Float('CYL', help='Left Eye Cylinder', states=STATES)
    raxis = fields.Float('Axis', help='Right Eye Axis', states=STATES)
    laxis = fields.Float('Axis', help='Left Eye Axis', states=STATES)
    rnv_add = fields.Float(
        'NV Add',
        help='Right Eye Best Corrected NV Add',
        states=STATES
    )
    lnv_add = fields.Float(
        'NV Add',
        help='Left Eye Best Corrected NV Add',
        states=STATES
    )
    rnv = fields.Selection(
        near_vision_chart,
        'RNV',
        help="Right Eye Near Vision",
        sort=False,
        states=STATES
    )
    lnv = fields.Selection(
        near_vision_chart,
        'LNV',
        help="Left Eye Near Vision",
        sort=False,
        states=STATES
    )
    rbcva_spherical = fields.Float(
        'SPH',
        help='Right Eye Best Corrected Spherical',
        states=STATES
    )
    lbcva_spherical = fields.Float(
        'SPH',
        help='Left Eye Best Corrected Spherical',
        states=STATES
    )
    rbcva_cylinder = fields.Float(
        'CYL',
        help='Right Eye Best Corrected Cylinder',
        states=STATES
    )
    lbcva_cylinder = fields.Float(
        'CYL',
        help='Left Eye Best Corrected Cylinder',
        states=STATES
    )
    rbcva_axis = fields.Float(
        'Axis',
        help='Right Eye Best Corrected Axis',
        states=STATES
    )
    lbcva_axis = fields.Float(
        'Axis',
        help='Left Eye Best Corrected Axis',
        states=STATES
    )
    rbcva = fields.Selection(
        snellen_chart,
        'RBCVA',
        help="Right Eye Best Corrected VA",
        sort=False,
        states=STATES
    )
    lbcva = fields.Selection(
        snellen_chart,
        'LBCVA',
        help="Left Eye Best Corrected VA",
        sort=False,
        states=STATES
    )
    rbcva_nv_add = fields.Float(
        'BCVA - Add',
        help='Right Eye Best Corrected NV Add',
        states=STATES
    )
    lbcva_nv_add = fields.Float(
        'BCVA - Add',
        help='Left Eye Best Corrected NV Add',
        states=STATES
    )
    rbcva_nv = fields.Selection(
        near_vision_chart,
        'RBCVANV',
        help="Right Eye Best Corrected Near Vision",
        sort=False,
        states=STATES
    )
    lbcva_nv = fields.Selection(
        near_vision_chart,
        'LBCVANV',
        help="Left Eye Best Corrected Near Vision",
        sort=False,
        states=STATES
    )
    notes = fields.Text('Notes', states=STATES)
    iop_method = fields.Selection(
        [
            ('nct', 'Non-contact tonometry'),
            ('schiotz', 'Schiotz tonometry'),
            ('goldmann', 'Goldman tonometry'),
        ],
        'Method',
        help='Tonometry/Intraocular pressure reading method',
        states=STATES
    )
    riop = fields.Float(
        'RIOP',
        digits=(2, 1),
        help="Right Intraocular Pressure in mmHg",
        states=STATES
    )
    liop = fields.Float(
        'LIOP',
        digits=(2, 1),
        help="Left Intraocular Pressure in mmHg",
        states=STATES
    )
    findings = fields.One2many(
        'ophthalmology.findings',
        'name',
        'Findings',
        states=STATES
    )
    state = fields.Selection(
        [
            ('in_progress', 'In progress'),
            ('done', 'Done'),
        ],
        'State',
        readonly=True,
        sort=False,
        default='in_progress'
    )
    signed_by = fields.Many2one(
        'res.partner',
        'Signed by',
        readonly=True,
        # states={'invisible': [('state','==', 'in_progress')]},
        help="Health Professional that finished the patient evaluation"
    )
    computed_age = fields.Char(string='Age')

    @api.onchange('patient')
    def patient_age_at_evaluation(self):
        if (self.patient.birthdate_date and self.visit_date):
            rdelta = relativedelta(
                self.visit_date.date(),
                self.patient.birthdate_date
            )
            years_months_days = str(rdelta.years) + 'y ' \
                + str(rdelta.months) + 'm ' \
                + str(rdelta.days) + 'd'
            self.computed_age = years_months_days
            return years_months_days
        else:
            return None

    @api.onchange('patient')
    def get_patient_gender(self):
        self.gender = self.patient.gender
        return self.patient.gender

    @api.onchange('patient')
    def on_change_patient(self):
        self.computed_age = self.patient.age
        return self.patient.age

    @api.onchange('rdva')
    def on_change_with_rbcva(self):
        return self.rdva

    @api.onchange('ldva')
    def on_change_with_lbcva(self):
        return self.ldva

    @api.onchange('rcylinder')
    def on_change_with_rbcva_cylinder(self):
        return self.rcylinder

    @api.onchange('lcylinder')
    def on_change_with_lbcva_cylinder(self):
        return self.lcylinder

    @api.onchange('raxis')
    def on_change_with_rbcva_axis(self):
        return self.raxis

    @api.onchange('laxis')
    def on_change_with_lbcva_axis(self):
        return self.laxis

    @api.onchange('rspherical')
    def on_change_with_rbcva_spherical(self):
        return self.rspherical

    @api.onchange('lspherical')
    def on_change_with_lbcva_spherical(self):
        return self.lspherical

    @api.onchange('rnv_add')
    def on_change_with_rbcva_nv_add(self):
        return self.rnv_add

    @api.onchange('lnv_add')
    def on_change_with_lbcva_nv_add(self):
        return self.lnv_add

    @api.onchange('rnv')
    def on_change_with_rbcva_nv(self):
        return self.rnv

    @api.onchange('lnv')
    def on_change_with_lbcva_nv(self):
        return self.lnv

    # Show the gender and age upon entering the patient
    # These two are function fields (don't exist at DB level)
    def end_evaluation(self):
        # Change the state of the evaluation to "Done"
        loging_user = self.env.user
        signing_hp = loging_user.partner_id
        self.state = 'done'
        self.signed_by = signing_hp
