# Copyright 2008 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>).
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPrescriptionOrderLine(models.Model):
    _name = 'medical.prescription.order.line'
    _inherit = ['abstract.medical.medication']
    _inherits = {'medical.patient.medication': 'medical_medication_id'}
    _rec_name = 'medical_medication_id'
    _description = 'Medical Prescription Order Line'

    prescription_order_id = fields.Many2one(
        comodel_name='medical.prescription.order',
        string='Prescription Order')
    medical_medication_id = fields.Many2one(
        comodel_name='medical.patient.medication', string='Medication',
        required=True, ondelete='cascade')
    is_substitutable = fields.Boolean()
    qty = fields.Float(string='Quantity')
