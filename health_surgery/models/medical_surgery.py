# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta


class MedicalRcri(models.Model):
    _name = 'medical.rcri'
    _description = 'Revised Cardiac Risk Index'

    patient = fields.Many2one(
        'medical.patient',
        'Patient ID',
        required=True
    )
    rcri_date = fields.Datetime(
        string='Date',
        required=True,
        default=datetime.now(),
    )
    health_professional = fields.Many2one(
        'medical.practitioner',
        'Health Professional',
        help="Health professional/Cardiologist who signed the assesment RCRI"
    )
    rcri_high_risk_surgery = fields.Boolean(
        'High Risk surgery',
        help='Suprainguinal vascular, intraperitoneal, or intrathoracic proc.'
    )
    rcri_ischemic_history = fields.Boolean(
        'History of ischemic heart disease',
        help="history of MI or a positive exercise test, current complaint of \
        of chest pain considered to be secondary to myocardial ischemia, use \
        of nitrate therapy, or ECG with pathological Q waves; do not count \
        prior coronary revascularization procedure unless one of the other \
        criteria for ischemic heart disease is present"
    )
    rcri_congestive_history = fields.Boolean(
        string='History of congestive heart disease'
    )
    rcri_diabetes_history = fields.Boolean(
        string='Preoperative Diabetes',
        help="Diabetes Mellitus requiring treatment with Insulin"
    )
    rcri_cerebrovascular_history = fields.Boolean(
        string='History of Cerebrovascular disease'
    )
    rcri_kidney_history = fields.Boolean(
        'Preoperative Kidney disease',
        help="Preoperative serum creatinine >2.0 mg/dL (177 mol/L)"
    )
    rcri_total = fields.Integer(
        'Score',
        help='Points 0: Class I Very Low (0.4% complications)\n\
        Points 1: Class II Low (0.9% complications)\n\
        Points 2: Class III Moderate (6.6% complications)\n\
        Points 3 or more : Class IV High (>11% complications)'
    )
    rcri_class = fields.Selection(
        [
            ('I', 'I'),
            ('II', 'II'),
            ('III', 'III'),
            ('IV', 'IV'),
        ],
        'RCRI Class',
        sort=False
    )

    @api.onchange(
        'rcri_high_risk_surgery', 'rcri_ischemic_history',
        'rcri_congestive_history', 'rcri_diabetes_history',
        'rcri_cerebrovascular_history', 'rcri_kidney_history'
    )
    def on_change_with_rcri_class(self):
        rcri_class = ''
        total = 0
        if self.rcri_high_risk_surgery:
            total = total + 1
        if self.rcri_ischemic_history:
            total = total + 1
        if self.rcri_congestive_history:
            total = total + 1
        if self.rcri_diabetes_history:
            total = total + 1
        if self.rcri_kidney_history:
            total = total + 1
        if self.rcri_cerebrovascular_history:
            total = total + 1
        self.rcri_total = total
        if total == 0:
            rcri_class = 'I'
        if total == 1:
            rcri_class = 'II'
        if total == 2:
            rcri_class = 'III'
        if (total > 2):
            rcri_class = 'IV'
        self.rcri_class = rcri_class

    def get_rec_name(self, name):
        res = 'Points: ' + str(self.rcri_total) + ' (Class ' + \
            str(self.rcri_class) + ')'
        return res

    def __setup__(self):
        super(MedicalRcri, self).__setup__()
        self._order.insert(0, ('rcri_date', 'DESC'))

    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op, ('patient',) + tuple(clause[1:])]


class MedicalSurgery(models.Model):
    _name = 'medical.surgery'
    _description = 'Surgery'
    _inherit = 'medical.abstract.entity'

    def surgery_duration(self, name):
        if (self.surgery_end_date and self.surgery_date):
            return self.surgery_end_date - self.surgery_date
        else:
            return None

    def patient_age_at_surgery(self, name):
        if (self.patient.name.dob and self.surgery_date):
            rdelta = relativedelta(
                self.surgery_date.date(), self.patient.name.dob
            )
            years_months_days = str(rdelta.years) + 'y ' \
                + str(rdelta.months) + 'm ' \
                + str(rdelta.days) + 'd'
            return years_months_days
        else:
            return None

    patient_id = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        required=True
    )
    admission = fields.Many2one(
        'medical.appointment',
        string='Admission'
    )
    operating_room = fields.Many2one(
        'medical.center',
        string='Operating Room'
    )
    code = fields.Char(
        'Code',
        readonly=True,
        help="Health Center code / sequence"
    )
    main_procedure = fields.Many2one(
        'medical.operation',
        'Main Proc',
        domain=[('name', '=', 'active_id')],
    )
    procedures = fields.One2many(
        comodel_name='medical.operation',
        inverse_name='name',
        string='Procedures',
        help="List of other procedures in the surgery."
    )
    supplies = fields.One2many(
        comodel_name='medical.surgery_supply',
        inverse_name='name',
        string='Supplies',
        help="List of the supplies required for the surgery"
    )
    pathology = fields.Many2one(
        comodel_name='medical.pathology',
        strin='Condition',
        help="Base Condition / Reason"
    )
    classification = fields.Selection(
        [
            ('o', 'Optional'),
            ('r', 'Required'),
            ('u', 'Urgent'),
            ('e', 'Emergency'),
        ],
        string='Urgency',
        help="Urgency level for this surgery",
        sort=False
    )
    surgeon = fields.Many2one(
        'medical.practitioner',
        'Surgeon',
        help="Surgeon who did the procedure"
    )
    anesthetist = fields.Many2one(
        'medical.practitioner',
        'Anesthetist',
        help="Anesthetist in charge"
    )
    surgery_date = fields.Datetime(
        string='Date',
        help="Start of the Surgery",
        default=datetime.now(),
    )
    surgery_end_date = fields.Datetime(
        'End',
        help="Automatically set when the surgery is done.\n\
        It is also the estimated end time when confirming the surgery."
    )
    surgery_length = fields.Datetime(
        'Duration',
        states={
            'done': [('invisible', True)], 'signed': [('invisible', True)]
        },
        help="Length of the surgery",
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('signed', 'Signed'),
        ],
        'State',
        readonly=True,
        sort=False,
        default='draft'
    )
    signed_by = fields.Many2one(
        'medical.practitioner',
        'Signed by',
        readonly=True,
        states={'signed': [('invisible', True)]},
        help="Health Professional that signed this surgery document"
    )
    computed_age = fields.Char(
        string='Age',
        help="Computed patient age at the moment of the surgery",
    )
    description = fields.Char(string='Description')
    preop_mallampati = fields.Selection(
        [
            (
                'Class 1',
                'Class 1: Full visibility of tonsils, uvula and soft palate'
            ), (
                'Class 2',
                'Class 2: Visibility of hard and soft palate, upper portion of\
                tonsils and uvula'
            ), (
                'Class 3',
                'Class 3: Soft and hard palate and base of the uvula are \
                visible'
            ), ('Class 4', 'Class 4: Only Hard Palate visible'),
        ],
        'Mallampati Score',
        sort=False
    )
    preop_bleeding_risk = fields.Boolean(
        'Risk of Massive bleeding',
        help="Patient has a risk of losing more than 500 "
        "ml in adults of over 7ml/kg in infants. If so, make sure that "
        "intravenous access and fluids are available"
    )
    preop_oximeter = fields.Boolean(
        'Pulse Oximeter in place',
        help="Pulse oximeter is in place "
        "and functioning"
    )
    preop_site_marking = fields.Boolean(
        'Surgical Site Marking',
        help="The surgeon has marked the surgical incision"
    )
    preop_antibiotics = fields.Boolean(
        'Antibiotic Prophylaxis',
        help="Prophylactic antibiotic treatment within the last 60 minutes"
    )
    preop_sterility = fields.Boolean(
        'Sterility confirmed',
        help="Nursing team has confirmed sterility of the devices and room"
    )
    preop_asa = fields.Selection(
        [
            ('ps1', 'PS 1 : Normal healthy patient'),
            ('ps2', 'PS 2 : Patients with mild systemic disease'),
            ('ps3', 'PS 3 : Patients with severe systemic disease'),
            (
                'ps4',
                'PS 4 : Patients with severe systemic disease that is a \
                constant threat to life'
            ), (
                'ps5',
                'PS 5 : Moribund patients who are not expected to survive \
                without the operation'
            ), (
                'ps6',
                'PS 6 : A declared brain-dead patient who organs are being \
                removed for donor purposes'
            ),
        ],
        'ASA PS',
        help="ASA pre-operative Physical Status",
        sort=False
    )
    preop_rcri = fields.Many2one(
        'medical.rcri',
        'RCRI',
        help='Patient Revised Cardiac Risk Index\n\
        Points 0: Class I Very Low (0.4% complications)\n\
        Points 1: Class II Low (0.9% complications)\n\
        Points 2: Class III Moderate (6.6% complications)\n\
        Points 3 or more : Class IV High (>11% complications)'
    )
    surgical_wound = fields.Selection(
        [
            ('I', 'Clean . Class I'),
            ('II', 'Clean-Contaminated . Class II'),
            ('III', 'Contaminated . Class III'),
            ('IV', 'Dirty-Infected . Class IV'),
        ],
        'Surgical wound',
        sort=False
    )
    extra_info = fields.Text(string='Extra Info')
    anesthesia_report = fields.Text(string='Anesthesia Report')
    institution = fields.Many2one('medical.center', string='Institution')
    report_surgery_date = fields.Datetime('Surgery date and time')
    surgery_team = fields.One2many(
        comodel_name='medical.surgery_team',
        inverse_name='partner_id',
        string='Team Members',
        help="Professionals Involved in the surgery"
    )
    postoperative_dx = fields.Many2one(
        comodel_name='medical.pathology',
        string='Post-op dx',
        states={
            'done': [('invisible', True)], 'signed': [('invisible', True)]
        },
        help="Post-operative diagnosis"
    )

    @api.model
    def create(self, vals):
        Sequence = self.env['ir.sequence']
        Config = self.env['medical.sequences']

        vals = [x.copy() for x in vals]
        for values in vals:
            if not values.get('code'):
                config = Config(1)
                values['code'] = Sequence.get_id(
                    config.surgery_code_sequence.id)
        return super(MedicalSurgery, self).create(vals)

    def write(self, surgeries, vals):
        # Don't allow to write the record if the surgery has been signed
        if surgeries[0].state == 'signed':
            self.raise_user_error(
                "This surgery is at state Done and has been signed\n"
                "You can no longer modify it.")
        return super(MedicalSurgery, self).write(surgeries, vals)

    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [
            bool_op, ('patient',) + tuple(clause[1:]),
            ('code',) + tuple(clause[1:]),
        ]


class MedicalOperation(models.Model):
    _name = 'medical.operation'
    _description = 'Operation - Surgical Procedures'

    name = fields.Many2one('medical.surgery', 'Surgery')
    procedure = fields.Many2one(
        'medical.procedure',
        'Code',
        required=True,
        index=True,
        help="Procedure Code, for example ICD-10-PCS or ICPM"
    )
    notes = fields.Text(string='Notes')


class SurgerySupply(models.Model):
    _name = 'medical.surgery_supply'
    _description = 'Supplies related to the surgery'

    name = fields.Many2one(
        'medical.surgery',
        'Surgery'
    )
    qty = fields.Integer(
        'Qty',
        required=True,
        help="Initial required quantity"
    )
    supply = fields.Many2one(
        'uom.uom',
        'Supply',
        required=True,
        domain=[('is_medical_supply', '=', True)],
        help="Supply to be used in this surgery"
    )
    notes = fields.Char(string='Notes')
    qty_used = fields.Integer(
        'Used',
        required=True,
        help="Actual amount used"
    )


class SurgeryTeam(models.Model):
    _name = 'medical.surgery_team'
    _inherit = 'medical.abstract.entity'
    _description = 'Team Involved in the surgery'

    name = fields.Many2one(
        'medical.surgery',
        'Surgery'
    )
    team_member = fields.Many2one(
        'medical.practitioner',
        'Member',
        required=True,
        index=True,
        help="Health professional that participated on this surgery"
    )
    role = fields.Many2one(
        comodel_name='medical.specialty',
        string='Role',
        domain=[('name', '=', 'team_member')],
    )
    notes = fields.Char(string='Notes')


class PatientData(models.Model):
    _name = 'medical.patient'
    _inherit = 'medical.patient'

    surgery = fields.One2many(
        comodel_name='medical.surgery',
        inverse_name='patient_id',
        string='Surgeries',
        readonly=True
    )
