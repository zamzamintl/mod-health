# Copyright 2008-2020 Luis Falcon <falcon@gnuhealth.org>.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class MedicalVaccination(models.Model):
    _name = 'medical.vaccination'
    _description = 'Patient Vaccination information'

    patient_id = fields.Many2one(
        'medical.patient',
        string='Patient',
        required=True,
    )
    vaccine_id = fields.Many2one(
        'medical.medicament',
        string='Vaccine',
        required=True,
        domain=[('is_vaccine', '=', True)],
        help='Vaccine Name. Make sure that the vaccine has all the'
        ' proper information at product level. Information such as provider,'
        ' supplier code, tracking number, etc.. This  information must always'
        ' be present. If available, please copy / scan the vaccine leaflet'
        ' and attach it to this record'
    )
    admin_route = fields.Selection(
        [
            ('im', 'Intramuscular'),
            ('sc', 'Subcutaneous'),
            ('id', 'Intradermal'),
            ('nas', 'Intranasal'),
            ('po', 'Oral'),
        ],
        'Route',
        sort=False
    )
    vaccine_expiration_date = fields.Date('Expiration date')
    vaccine_lot = fields.Char(
        'Lot Number',
        help='Please check on the vaccine (product) production lot number and'
        ' tracking number when available!'
    )
    institution_id = fields.Many2one(
        'medical.center',
        'Medical Center',
        index=True,
        domain=[('is_institution', '=', True)],
        help='Medical Center where the patient is being or was vaccinated',
    )
    date = fields.Datetime('Date')
    dose = fields.Integer('Dose')
    next_dose_date = fields.Datetime('Next Dose')
    observations = fields.Text('Observations')
    healthprof_id = fields.Many2one(
        'medical.practitioner',
        'Health Prof',
        readonly=True,
        help="Health Professional who administered or reviewed the vaccine \
        information"
    )
    signed_by = fields.Many2one(
        'medical.practitioner',
        'Signed by',
        readonly=True,
        help="Health Professional that signed the vaccination document"
    )
    amount = fields.Float(
        'Amount',
        help='Amount of vaccine administered, in mL . The dose per mL \
        (eg, mcg, EL.U ..) can be found at the related medicament'
    )
    admin_site = fields.Selection(
        [
            ('lvl', 'left vastus lateralis'),
            ('rvl', 'right vastus lateralis'),
            ('ld', 'left deltoid'),
            ('rd', 'right deltoid'),
            ('lalt', 'left anterolateral fat of thigh'),
            ('ralt', 'right anterolateral fat of thigh'),
            ('lpua', 'left posterolateral fat of upper arm'),
            ('rpua', 'right posterolateral fat of upper arm'),
            ('lfa', 'left fore arm'),
            ('rfa', 'right fore arm')
        ],
        'Admin Site'
    )
    state = fields.Selection(
        [
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
        ],
        'State',
        default='in_progress'
    )

    def action_validate(self):
        self.ensure_one()
        self.write({'state': 'done'})
