# Copyright 2015 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api


class MedicalPharmacy(models.Model):
    """Medical pharmacy attributes on res.partner"""
    _name = 'medical.pharmacy'
    _description = 'Medical Pharmacy'
    _inherits = {'res.partner': 'partner_id', }

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        ondelete='cascade',
        index=True,
    )

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        vals['is_pharmacy'] = True
        return super(MedicalPharmacy, self).create(vals)

    def onchange_state(self, state_id):
        return self.partner_id.onchange_state(state_id)

    def onchange_address(self, use_parent_address, parent_id, ):
        return self.partner_id.onchange_address(use_parent_address, parent_id)
