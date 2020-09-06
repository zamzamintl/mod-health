# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPharmacy(models.Model):
    _inherit = 'medical.pharmacy'

    nabp_num = fields.Integer(string='National Boards of Pharmacy Id #')
    medicaid_num = fields.Integer(string='Medicaid Id #')
    npi_num = fields.Integer(string="National Provider Identifier")
