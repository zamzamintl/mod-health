# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta


class ContactMechanism(models.Model):
    _name = 'partner.contact.mechanism'
    _description = 'Contact Mechanism'

    emergency = fields.Boolean(
        string='Emergency',
        index=True
    )
    remarks = fields.Char(
        string='Remarks',
        help="Enter the name of the contact or other remarks"
    )


class PersonName(models.Model):
    _name = 'medical.person.name'
    _description = "Person Name"

    partner_id = fields.Many2one(
        'res.partner',
        string='Person',
        domain=[('is_person', '=', True)],
        help="Related partner (person)"
    )
    use = fields.Selection(
        [
            ('official', 'Official'),
            ('usual', 'Usual'),
            ('nickname', 'Nickname'),
            ('maiden', 'Maiden'),
            ('anonymous', 'Anonymous'),
            ('temp', 'Temp'),
            ('old', 'old'),
        ],
        'Use',
        sort=False,
        required=True
    )
    family = fields.Char(
        string='Family',
        help="Family / Surname."
    )
    given = fields.Char(
        string='Given',
        help="Given / First name. May include middle name",
        required=True
    )
    prefix = fields.Selection(
        [
            ('Mr', 'Mr'),
            ('Mrs', 'Mrs'),
            ('Miss', 'Miss'),
            ('Dr', 'Dr'),
        ],
        string='Prefix',
        sort=False
    )
    suffix = fields.Char(string='Suffix')
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')


class FamilyAddress(models.Model):
    _name = 'family.address'
    _description = 'Family Address'

    relationship = fields.Char(
        string='Relationship',
        help='Relationship with the person (friend, co-worker, brother)'
    )
    relative_id = fields.Many2one(
        'res.partner',
        'Contact',
        domain=[('is_person', '=', True)],
        help='Include link to the relative'
    )
    is_school = fields.Boolean(
        "School",
        help="Check this box to mark the school address"
    )
    is_work = fields.Boolean(
        "Work",
        help="Check this box to mark the work address"
    )


class Occupation(models.Model):
    _name = 'medical.occupation'
    _description = 'Occupation'

    name = fields.Char(
        'Name',
        required=True,
        translate=True
    )
    code = fields.Char(
        string='Code',
        required=True,
        help="Please use CAPITAL LETTERS and no spaces"
    )
    profession = fields.Char(string='Profesión')
    # occupation = fields.Many2one(
    #     'res.occupation',
    #     'Oficio actual'
    # )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'El nombre debe ser único'
        ), (
            'code_uniq',
            'unique(code)',
            'El código debe ser único'
        )
    ]


class Ethnicity(models.Model):
    _name = 'medical.ethnicity'
    _description = 'Ethnicity'

    name = fields.Char(
        string='Ethnicity',
        required=True,
        translate=True
    )
    code = fields.Char(
        string='Code',
        required=True,
        help="Please use CAPITAL LETTERS and no spaces"
    )
    notes = fields.Char('Notes')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'El nombre debe ser único'
        ), (
            'code_uniq',
            'unique(code)',
            'El código debe ser único'
        )
    ]


class Family(models.Model):
    _name = 'medical.family'
    _description = 'Family'

    name = fields.Char(
        string='Family',
        required=True,
        help='Family code'
    )
    members = fields.One2many(
        comodel_name='medical.family.member',
        inverse_name='name',
        string='Family Members'
    )
    info = fields.Text(string='Extra Information')

    _sql_constraints = [
        (
            'code_uniq',
            'unique(name)',
            'El código de Familia debe ser único'
        )
    ]


class FamilyMember(models.Model):
    _name = 'medical.family.member'
    _description = 'Family Member'

    name = fields.Many2one(
        'medical.family',
        'Family',
        required=True,
        readonly=True,
        help='Family code'
    )
    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        required=True,
        domain=[('is_person', '=', True)],
        help='Family Member'
    )
    role = fields.Char(
        string='Role',
        help='Father, Mother, sibbling...'
    )


class BirthCertExtraInfo (models.Model):
    _name = 'medical.birth.certificate'
    _description = 'Birth Certificate'

    institution = fields.Many2one(
        'medical.institution',
        'Institution',
    )
    signed_by = fields.Many2one(
        string='Certifier',
        comodel_name='medical.healthprofessional',
        help='Person who certifies this birth document',
        readonly=True,
    )
    certification_date = fields.Datetime(
        string='Signed on',
        readonly=True,
    )

    # def default_institution():
    #     return HealthInstitution().get_institution()

    # Esto probablemente se refiera a país y estado. Simplificar.
    @api.depends('institution')
    def on_change_institution(self):
        country = None
        subdivision = None
        if (self.institution and self.institution.name.addresses[0].country):
            country = self.institution.name.addresses[0].country.id
        if (
            self.institution and
            self.institution.name.addresses[0].subdivision
        ):
            subdivision = self.institution.name.addresses[0].subdivision.id
        self.country = country
        self.country_subdivision = subdivision

    def sign(self, certificates):
        HealthProfessional = self.env['medical.healthprofessional']
        Person = self.env['res.partner']
        partner = []

        # Change the state of the birth certificate to "Signed"
        # and write the name of the certifying health professional
        signing_hp = HealthProfessional.get_health_professional()
        if not signing_hp:
            self.raise_user_error(
                "No health professional associated to this user!"
            )
        self.write(certificates, {
            'state': 'signed',
            'signed_by': signing_hp,
            'certification_date': datetime.now()}
        )
        partner.append(certificates[0].name)
        Person.write(partner, {
            'birth_certificate': certificates[0].id}
        )


class DeathCertExtraInfo (models.Model):
    _name = 'medical.death.certificate'
    _description = 'Death Certificate'

    institution = fields.Many2one(
        'medical.institution',
        'Institution',
    )
    signed_by = fields.Many2one(
        'medical.healthprofessional', 'Signed by', readonly=True,
        help="Health Professional that signed the death certificate"
    )
    certification_date = fields.Datetime('Certified on', readonly=True)
    cod = fields.Many2one(
        'medical.pathology',
        'Cause',
        required=True,
        help="Immediate Cause of Death",
    )
    # underlying_conditions = fields.One2many(
    #     'medical.death_underlying_condition',
    #     'death_certificate',
    #     'Underlying Conditions',
    #     help='Underlying conditions that initiated the events resulting in '
    #     'death. Please code them in sequential, chronological order'
    # )

    # def default_institution():
    #     return HealthInstitution().get_institution()

    def default_state():
        return 'draft'

    @api.depends('institution')
    def on_change_institution(self):
        country = None
        subdivision = None
        if (self.institution and self.institution.name.addresses[0].country):
            country = self.institution.name.addresses[0].country.id
        if (
            self.institution and
            self.institution.name.addresses[0].subdivision
        ):
            subdivision = self.institution.name.addresses[0].subdivision.id
        self.country = country
        self.country_subdivision = subdivision

    def sign(self, certificates):
        HealthProfessional = self.env['medical.healthprofessional']
        Person = self.env['res.partner']

        # Change the state of the death certificate to "Signed"
        # and write the name of the certifying health professional
        # It also set the associated partner attribute deceased to True.
        partner = []
        signing_hp = HealthProfessional.get_health_professional()
        if not signing_hp:
            self.raise_user_error(
                "No health professional associated to this user!"
            )
        self.write(certificates, {
            'state': 'signed',
            'signed_by': signing_hp,
            'certification_date': datetime.now()}
        )
        partner.append(certificates[0].name)
        Person.write(partner, {
            'deceased': True,
            'death_certificate': certificates[0].id
        })


class InsurancePlan(models.Model):
    _inherit = 'medical.insurance.plan'

    is_default = fields.Boolean(
        'Default plan',
        help='Check if this is the default plan when assigning this insurance'
        ' company to a patient'
    )


class Insurance(models.Model):
    _name = 'medical.insurance'
    _description = 'Insurance'
    _rec_name = 'number'

    # Insurance associated to an individual
    name = fields.Many2one("res.partner", string='Owner')
    number = fields.Char(string='Number', required=True)
    company = fields.Many2one(
        'res.partner',
        'Insurance Company',
        required=True,
        index=True,
        domain=[('is_insurance_company', '=', True)]
    )
    member_since = fields.Date(string='Member since')
    member_exp = fields.Date(string='Expiration date')
    category = fields.Char('Category', help='Insurance company category')
    insurance_type = fields.Selection(
        [
            ('state', 'State'),
            ('labour_union', 'Labour Union / Syndical'),
            ('private', 'Private'),
        ],
        'Insurance Type',
        index=True
    )
    plan_id = fields.Many2one(
        'medical.insurance.plan', 'Plan',
        help='Insurance company plan',
        domain=[('company', '=', 'company')]
    )
    notes = fields.Text(string='Insurance Extra Info')

    def get_rec_name(self, name):
        return (self.company.name + ' : ' + self.number)

    _sql_constraints = [(
        'number_uniq',
        'unique(number)',
        'The number must be unique per insurance company'
    )]


class AlternativePersonID (models.Model):
    _name = 'medical.person.alternative.identification'
    _description = 'Alternative person ID'

    name = fields.Many2one(
        'res.partner', 'Partner',
        readonly=True)
    code = fields.Char(string='Code', required=True)
    alternative_id_type = fields.Selection(
        [
            ('country_id', 'Country of origin ID'),
            ('passport', 'Passport'),
            ('medical_record', 'Medical Record'),
            ('ghealth_federation', 'GNU Health Federation'),
            ('other', 'Other'),
        ],
        'ID type',
        required=True,
        sort=False
    )
    comments = fields.Char(string='Comments')


class BirthCertificate (models.Model):
    _name = 'medical.birth.certificate'
    _description = 'Birth Certificate'

    name = fields.Many2one(
        'res.partner',
        'Person',
        required=True,
        domain=[('is_person', '=', True)]
    )
    mother = fields.Many2one(
        'res.partner',
        'Mother',
        domain=[('is_person', '=', True)]
    )
    father = fields.Many2one(
        'res.partner',
        'Father',
        domain=[('is_person', '=', True)]
    )
    code = fields.Char('Code', required=True)
    dob = fields.Date('Date of Birth', required=True)
    observations = fields.Text('Observations',)
    address_country = fields.Many2one(
        'res.country',
        'Country',
        required=True,
    )
    address_city = fields.Many2one(
        'res.country.state',
        string='State'
        )
    address_municipaly = fields.Many2one(
        'res.country.state.municipality',
        string='Municipaly',
    )
    address_parish = fields.Many2one(
        'res.country.state.municipality.parish',
        string='Parish'
    )
    address_zip = fields.Char(string='Postal Code')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('signed', 'Signed'),
            ('done', 'Done'),
        ],
        'State',
        readonly=True,
        sort=False
    )

    def default_state():
        return 'draft'

    @api.depends('name')
    def on_change_with_dob(self):
        if (self.name and self.name.dob):
            dob = self.name.dob
            return dob

    _sql_constraints = [
        (
            'name_unique',
            'unique(name)',
            'Certificate already exists !'
        ), (
            'code_unique',
            'unique(code)',
            'Certificate already exists !'
        )
    ]

    def setUp(self, certificates):
        super(BirthCertificate, self).setUp(certificates)
        for certificate in certificates:
            certificate.validate_dob()

    def validate_dob(self):
        if (self.name.dob != self.dob):
            self.raise_user_error(
                "The date on the Partner differs from the certificate!"
            )


class DeathCertificate (models.Model):
    _name = 'medical.death.certificate'
    _description = 'Death Certificate'

    name = fields.Many2one(
        'res.partner',
        'Person',
        required=True,
        domain=[('is_person', '=', True)]
    )
    code = fields.Char(string='Code', required=True)
    autopsy = fields.Boolean(
        string='Autopsy',
        help="Check this box if autopsy has been done"
    )
    dod = fields.Datetime(
        string='Date',
        required=True,
        help="Date and time of Death",
    )
    type_of_death = fields.Selection(
        [
            ('natural', 'Natural'),
            ('suicide', 'Suicide'),
            ('homicide', 'Homicide'),
            ('undetermined', 'Undetermined'),
            ('pending_investigation', 'Pending Investigation'),
        ],
        'Type of death',
        required=True,
        sort=False
    )
    place_of_death = fields.Selection(
        [
            ('home', 'Home'),
            ('work', 'Work'),
            ('public_place', 'Public place'),
            ('health_center', 'Health Center'),
        ],
        'Place',
        required=True,
        sort=False,
    )
    # operational_sector = fields.Many2one(
    #     'medical.operational_sector',
    #     'Op. Sector',
    # )
    du = fields.Many2one(
        'housing.du',
        'DU',
        help="Domiciliary Unit",
    )
    place_details = fields.Char('Details')
    address_country = fields.Many2one(
        'res.country',
        'Country',
        required=True,
    )
    address_city = fields.Many2one(
        'res.country.state',
        string='State'
        )
    address_municipaly = fields.Many2one(
        'res.country.state.municipality',
        string='Municipaly',
    )
    address_parish = fields.Many2one(
        'res.country.state.municipality.parish',
        string='Parish'
    )
    address_zip = fields.Char(string='Postal Code')
    age = fields.Char(string='Age')
    observations = fields.Text(string='Observations')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('signed', 'Signed'),
            ('done', 'Done'),
        ],
        'State',
        readonly=True,
        sort=False
    )

    def default_state():
        return 'draft'

    _sql_constraints = [
        (
            'name_unique',
            'unique(name)',
            'Certificate already exists !'
        ), (
            'code_unique',
            'unique(code)',
            'Certificate already exists !'
        )
    ]

    def get_age_at_death(self, name):
        if (self.name.dob):
            delta = relativedelta(self.dod, self.name.dob)
            years_months_days = str(delta.years) + 'y ' \
                + str(delta.months) + 'm ' \
                + str(delta.days) + 'd'
        else:
            years_months_days = None
        return years_months_days


# UNDERLYING CONDITIONS THAT RESULT IN DEATH INCLUDED IN DEATH CERT.
class DeathUnderlyingCondition(models.Model):
    _name = 'medical.death.underlying.condition'
    _description = 'Underlying Conditions'

    death_certificate = fields.Many2one(
        string='Certificate',
        comodel_name='medical.death.certificate',
        readonly=True
    )
    condition = fields.Many2one(
        'medical.pathology',
        'Condition',
        required=True
    )
    interval = fields.Integer(
        'Interval',
        help='Approx Interval onset to death',
        required=True
    )
    unit_of_time = fields.Selection(
        [
            ('minutes', 'minutes'),
            ('hours', 'hours'),
            ('days', 'days'),
            ('months', 'months'),
            ('years', 'years'),
        ],
        'Unit',
        index=True,
        sort=False,
        required=True
    )
