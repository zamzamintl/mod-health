# Copyright 2017 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html)

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    patient_id = fields.Many2one(
        string='Patient',
        comodel_name='medical.patient',
        related='prescription_order_line_id.patient_id',
    )
    prescription_order_line_id = fields.Many2one(
        string='Prescription Line',
        comodel_name='medical.prescription.order.line',
    )
    medication_id = fields.Many2one(
        string='Medication',
        comodel_name='medical.patient.medication',
        related='prescription_order_line_id.medical_medication_id',
    )
