# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    housing = fields.Many2one('housing.du', ondelete='CASCADE')
