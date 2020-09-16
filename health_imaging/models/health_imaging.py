# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api
import datetime


class ImagingTestType(models.Model):
    """Imaging Test Type"""
    _name = 'imaging.test.type'
    _description = 'Imaging Test Type'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)


class ImagingTest(models.Model, ):
    """Imaging Test"""
    _name = 'imaging.test'
    _description = 'Imaging Test'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    test_type = fields.Many2one(
        'imaging.test.type',
        'Type',
        required=True
    )
    product = fields.Many2one('product.product', 'Service', required=True)
    active = fields.Boolean('Active', index=True, default=True)


class ImagingTestRequest(models.Model):
    """Imaging Test Request"""
    _name = 'imaging.test.request'
    _description = 'Imaging Test Request'

    patient = fields.Many2one('medical.patient', 'Patient', required=True)
    date = fields.Datetime(
        'Date',
        required=True,
        default=datetime.date.today()
    )
    requested_test = fields.Many2one(
        'imaging.test',
        'Test',
        required=True
    )
    doctor = fields.Many2one('res.partner', 'Doctor', required=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('requested', 'Requested'),
            ('done', 'Done'),
        ],
        'State',
        default='draft'
    )
    comment = fields.Text('Comment')
    name = fields.Char(
        'Request',
        readonly=True,
        required=True,
        copy=False,
        default='New'
    )
    urgent = fields.Boolean('Urgent')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'imaging.test.request') or 'New'
        result = super(ImagingTestRequest, self).create(vals)
        return result

    def copy(self, tests, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['request'] = None
        default['date'] = datetime.date.today()
        return super(ImagingTestRequest, self).copy(tests, default=default)

    def requested(self):
        self.state = 'requested'

    def generate_results(self):
        """This opens the xml view specified in xml_id"""
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].\
                for_xml_id('health_imaging', xml_id)
            res.update(
                context=dict(
                    self.env.context,
                    default_patient=self.patient.id,
                    default_requested_test=self.requested_test.id,
                    default_request=self.id,
                    default_request_date=self.date,
                    group_by=False
                ),
                domain=[('patient', '=', self.patient.id)]
            )
            return res
        return False

    def done(self):
        self.state = 'done'


class ImagingTestResult(models.Model):
    """Imaging Test Result"""
    _name = 'imaging.test.result'
    _description = 'Imaging Test Result'
    _inherit = ['image.mixin']

    name = fields.Char(
        'Number',
        readonly=True,
        required=True,
        copy=False,
        default='New'
    )
    patient = fields.Many2one('medical.patient', 'Patient', readonly=True)
    date = fields.Datetime('Date', required=True)
    request_date = fields.Datetime('Requested Date', readonly=True)
    requested_test = fields.Many2one(
        'imaging.test',
        'Test',
        required=True
    )
    request = fields.Many2one(
        'imaging.test.request',
        'Request',
        readonly=True
    )
    doctor = fields.Many2one('res.partner', 'Doctor', required=True)
    comment = fields.Text('Comment')
    images = fields.Many2many(
        comodel_name="ir.attachment",
        relation="m2m_ir_attachment_relation",
        column1="m2m_id",
        column2="attachment_id",
        string="Attachments"
    )
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'The test ID code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'imaging.test.result'
            ) or 'New'
            result = super(ImagingTestResult, self).create(vals)
            return result

    @classmethod
    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [
            bool_op,
            ('patient',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
        ]
