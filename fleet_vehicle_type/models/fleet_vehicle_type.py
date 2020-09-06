# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class FleetVehicleType(models.Model):
    _name = 'fleet.vehicle.type'
    _description = 'Types of vehicles'

    name = fields.Char(string='Type')
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
