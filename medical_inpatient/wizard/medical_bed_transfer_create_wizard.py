# Copyright (C) 2008-2019 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2019 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools.translate import _

__all__ = ['CreateBedTransfer']


class CreateBedTransfer(models.TransientModel):
    """
    Create Bed Transfer.
    """
    _name = 'medical.bed.transfer.create'
    _description = 'Create Bed Transfer'
    newbed = fields.Many2one(
        'hospital.bed',
        'New Bed',
        required=True,
        index=True
    )
    reason = fields.Char(
        'Reason',
        required=True
    )
    orig_bed_state = fields.Selection(
        [
            ('none', ''),
            ('free', 'Free'),
            ('reserved', 'Reserved'),
            ('occupied', 'Occupied'),
            ('to_clean', 'Needs cleaning'),
            ('na', 'Not available'),
        ], 'Bed of origin Status',
        sort=False,
        default='to_clean',
        required=True
    )
    def button_create_bed_transfer(self):
        inpatient_registrations = self.env['medical.inpatient_registration']
        bed = self.env['hospital.bed']
        registrations = inpatient_registrations.browse(self.env.context['active_ids'])
        # Don't allow mass changes. Work on a single record
        if len(registrations) > 1:
            raise UserError(
                _(
                    'You have chosen more than 1 records. Please choose only one!'
                ))
        registration = registrations[0]
        current_bed = registration.bed
        destination_bed = self.newbed
        reason = self.reason
        orig_bed_state = self.orig_bed_state
        # Check that the new bed is free
        if destination_bed.state == 'free':
            # Update bed status with the one given in the transfer
            current_bed.write({'state': orig_bed_state})
            # Set as occupied the new bed
            destination_bed.write({'state': 'occupied'})
            # Update the hospitalization record
            hospitalization_info = {}
            hospitalization_info['bed'] = destination_bed
            # Update the hospitalization data
            transfers = []
            transfers.append(('create', [{
                'transfer_date': datetime.now(),
                'bed_from': current_bed.id,
                'bed_to': destination_bed.id,
                'reason': reason,
            }]))
            hospitalization_info['bed_transfers'] = transfers
            registration.write(hospitalization_info)
        else:
            raise UserError(
                _(
                    'Destination bed is unavailable!'
                ))
        return {'type': 'ir.actions.act_window_close'}
