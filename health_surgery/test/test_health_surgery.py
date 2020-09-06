# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo.tests.common import TransactionCase


class TestHealthSurgery(TransactionCase):
	def setUp(self,):
		super(TestHealthSurgery, self).setUp()
		self.model_obj = self.env['health.surgery']
		self.vals = {'name': 'Test Health Surgery'}
