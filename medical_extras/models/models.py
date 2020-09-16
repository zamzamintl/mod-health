# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api


class MedicalAppointment(models.Model):
    _name = 'medical.appointment'
    _inherit = 'appointment'
    _description = 'Patient Appointments'
    _order = "app_date desc"

    speciality = fields.Many2one(
        'medical.specialty',
        'Specialty',
        help='Medical Specialty / Sector'
    )
    state = fields.Selection(
        [
            ('free', 'Free'),
            ('confirmed', 'Confirmed'),
            ('checked_in', 'Checked in'),
            ('done', 'Done'),
            ('user_cancelled', 'Cancelled by patient'),
            ('center_cancelled', 'Cancelled by Health Center'),
            ('no_show', 'No show')
        ],
        'State',
        default='confirmed',
        sort=False
    )
    urgency = fields.Selection(
        [
            ('a', 'Normal'),
            ('b', 'Urgent'),
            ('c', 'Medical Emergency')
        ],
        'Urgency',
        default='a',
        sort=False
    )
    comments = fields.Text('Comments')
    appointment_type = fields.Selection(
        [
            ('none', ''),
            ('outpatient', 'Outpatient'),
            ('inpatient', 'Inpatient'),
        ],
        'Type',
        default='outpatient',
        sort=False
    )
    visit_type = fields.Selection(
        [
            ('new', 'New health condition'),
            ('followup', 'Followup'),
            ('well_child', 'Well Child visit'),
            ('well_woman', 'Well Woman visit'),
            ('well_man', 'Well Man visit')
        ],
        'Visit',
        sort=False
    )
    consultations = fields.Many2one(
        'product.product',
        'Consultation Services',
        domain=[('type', '=', 'service')],
        help='Consultation Services'
    )

    def checked_in(self):
        self.ensure_one()
        self.write({'state': 'checked_in'})

    def no_show(self):
        self.ensure_one()
        self.write({'state': 'no_show'})

    @api.onchange('patient')
    def on_change_patient(self):
        if self.patient:
            self.state = 'confirmed'
        else:
            self.state = 'free'


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medical_supply = fields.Boolean('Medical Supply')
    is_bed = fields.Boolean('Bed', help='Check if the product is a bed')


class Medicament(models.Model):
    _inherit = "medical.medicament"

    strength = fields.Float('Strength', help='Amount of medication per dose')
    sol_conc = fields.Float('Concentration', help='Solution concentration')
    sol_vol = fields.Float('Volume', help='Solution concentration volume')
    presentation = fields.Text('Presentation', help='Packaging')
    storage = fields.Text('Storage Conditions')
