# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

#from trytond.modules.company import CompanyReport
from odoo import models

__all__ = ['LabTestReport']

class LabTestReport(models.Models):
    __name__ = 'patient.labtest.report'
