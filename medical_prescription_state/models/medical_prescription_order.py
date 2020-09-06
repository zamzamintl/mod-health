# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class MedicalPrescriptionOrder(models.Model):
    _inherit = 'medical.prescription.order'
    _order = 'priority desc, sequence, date_prescription, name'

    sequence = fields.Integer(
        default=10,
        help="Sequence order when displaying a list of Rxs",
    )
    priority = fields.Selection(
        [
            ('0', 'Normal'),
            ('5', 'Medium'),
            ('10', 'High'),
        ],
        index=True,
    )
    state_id = fields.Many2one(
        'medical.prescription.order.state',
        'State',
        track_visibility='onchange',
        index=True,
        copy=False,
    )
    user_id = fields.Many2one(
        'res.users',
        'Assigned To',
        index=True,
        track_visibility='onchange',
    )
    date_assign = fields.Datetime('Assigned Date')
    legend_blocked = fields.Char(
        string='Kanban Blocked Explanation',
        related='state_id.legend_blocked'
    )
    legend_done = fields.Char(
        string='Kanban Valid Explanation',
        related='state_id.legend_done'
    )
    legend_normal = fields.Char(
        string='Kanban Ongoing Explanation',
        related='state_id.legend_normal'
    )
    color = fields.Integer('Color Select')
    kanban_state = fields.Selection(
        [
            ('normal', 'In Progress'),
            ('done', 'Ready for next stage'),
            ('blocked', 'Blocked')
        ],
        'Kanban State',
        default='normal',
        track_visibility='onchange',
        required=True,
        copy=False,
        help="An Rx's kanban state indicates special situations affecting it:"
        "\n * Normal is the default situation"
        "\n * Blocked indicates something is preventing the progress of this"
        " Rx"
        "\n * Ready for next stage indicates the Rx is ready to be pulled to"
        " the next stage",
    )
