# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPrescriptionOrderState(models.Model):
    _name = 'medical.prescription.order.state'
    _description = 'Prescription Order States'

    name = fields.Char(
        'State Name',
        required=True,
    )
    description = fields.Text('Description')
    sequence = fields.Integer(
        'Sequence',
        default=1,
    )
    legend_priority = fields.Char(
        'Priority Management Explanation',
        help='Explanation text to help users using the star and priority'
        ' mechanism on stages or RXs that are in this stage.',
    )
    legend_blocked = fields.Char(
        'Kanban Blocked Explanation',
        help='Override the default value displayed for the blocked state for'
        ' kanban selection, when the RX is in that stage.',
    )
    legend_done = fields.Char(
        'Kanban Valid Explanation',
        help='Override the default value displayed for the done state for'
        ' kanban selection, when the RX is in that stage.',
    )
    legend_normal = fields.Char(
        'Kanban Ongoing Explanation',
        help='Override the default value displayed for the normal state for'
        ' kanban selection, when the RX is in that stage.',
    )
    fold = fields.Boolean(
        'Folded in RX Pipeline',
        help='This stage is folded in the kanban view when'
        ' there are no records in that stage to display.',
    )
    color = fields.Integer(
        'Color Index',
        help='Color index to be used if the Rx does not have one defined'
    )
