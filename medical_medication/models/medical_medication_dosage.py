# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2015 Acsone.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalMedicationDosage(models.Model):
    _name = 'medical.medication.dosage'
    _description = 'Medical Medication Dosage'

    name = fields.Char(required=True, translate=True)
    abbreviation = fields.Char(
        help='Dosage abbreviation, such as tid in the US or tds in the UK')
    code = fields.Char(
        help='Dosage Code,for example: SNOMED 229798009 = 3 times per day')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Name must be unique!'),
    ]
