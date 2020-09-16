# Copyright (C) 2008-2019 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2019 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools.translate import _

__all__ = ['CreateInpatientEvaluation']


class CreateInpatientEvaluation(models.TransientModel):
    """
    Create Inpatient Evaluation.
    """
    _name = 'medical.inpatient.evaluation.create'
    _description = 'Create Inpatient Evaluation'
    def do_inpatient_evaluation(self):
        self.ensure_one()
        inpatient_registrations = self.env['medical.inpatient_registration']
        registrations = inpatient_registrations.browse(self.env.context['active_id'])
        if not registrations:
            raise UserError(
                _(
                    'You need to select an inpatient registration record!'
                ))
        patient = registrations[0].patient.id
        inpatient_registration_code = registrations[0].id
        evaluation_type = 'inpatient'
        view_id = self.env.ref('medical.medical_patient_evaluation_view').id
        return {
            'name': _('Patient Evaluation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'medical.patient.evaluation',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_patient': patient,
                'default_inpatient_registration_code': inpatient_registration_code,
                'default_evaluation_type': evaluation_type,
            }
        }
