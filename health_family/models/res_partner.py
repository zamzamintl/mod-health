# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta
import random


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def compute_age_from_dates(dob, deceased, dod, gender, caller, extra_date):
        """ Get the person's age.
            Calculate the current age of the patient or age at time of death.
            Returns:
            If caller == 'age': str in Y-M-D,
                caller == 'childbearing_age': boolean,
                caller == 'raw_age': [Y, M, D] """
        today = datetime.today().date()
        if dob:
            start = datetime.strptime(str(dob), '%Y-%m-%d')
            end = datetime.strptime(str(today), '%Y-%m-%d')
            if extra_date:
                end = datetime.strptime(str(extra_date), '%Y-%m-%d')
            if deceased and dod:
                end = datetime.strptime(
                            str(dod), '%Y-%m-%d %H:%M:%S')
            rdelta = relativedelta(end, start)
            years_months_days = str(rdelta.years) + 'y ' \
                + str(rdelta.months) + 'm ' \
                + str(rdelta.days) + 'd'
        else:
            return None
        if caller == 'age':
            return years_months_days
        elif caller == 'childbearing_age':
            if (rdelta.years >= 11
               and rdelta.years <= 55 and gender == 'f'):
                return True
            else:
                return False
        elif caller == 'raw_age':
            return [rdelta.years, rdelta.months, rdelta.days]
        else:
            return None

    def person_age(self, name):
        return self.compute_age_from_dates(
            self.dob, self.deceased, self.dod, self.gender, name, None
        )

    def get_du_address(self, name):
        if (self.du):
            return self.du.address_repr

    person_names = fields.One2many(
        comodel_name='medical.person.name',
        inverse_name='partner_id',
        string='Person Names',
        # states={'invisible': 'is_person'}
    )
    name_representation = fields.Selection(
        [
            ('pgfs', 'Prefix Given Family, Suffix'),
            ('gf', 'Given Family'),
            ('fg', 'Family, Given'),
            ('cjk', 'CJK: Family+Given'),
        ],
        string='Name Representation',
        sort=False,
        states={'invisible': 'is_person'}
    )
    activation_date = fields.Date(
        string='Activation date',
        help='Date of activation of the partner'
    )
    ref = fields.Char(
        string='PUID',
        help='Person Unique Identifier',
        states={'invisible': 'is_person'}
    )
    unidentified = fields.Boolean(
        string='Unidentified',
        help='Patient is currently unidentified',
        states={'invisible': 'is_person'}
    )
    is_person = fields.Boolean(
        string='Person',
        help='Check if the partner is a person.'
    )
    is_patient = fields.Boolean(
        string='Patient',
        states={'invisible': 'is_person'},
        help='Check if the partner is a patient'
    )
    is_healthprof = fields.Boolean(
        string='Health Prof',
        states={'invisible': 'is_person'},
        help='Check if the partner is a health professional'
    )
    is_insurance_company = fields.Boolean(
        string='Insurance Company',
        help='Check if the partner is an Insurance Company'
    )
    is_pharmacy = fields.Boolean(
        string='Pharmacy',
        help='Check if the partner is a Pharmacy'
    )
    lastname = fields.Char(
        string='Family names',
        help='Family or last names',
        states={'invisible': 'is_person'}
    )
    dob = fields.Date(string='DoB', help='Date of Birth')
    age = fields.Char(
        compute='_compute_age',
        string='Age (compute)'
    )
    photo = fields.Binary('Picture')
    ethnic_group = fields.Many2one(
        'medical.ethnicity',
        string='Ethnicity'
    )
    address_country = fields.Many2one(
        'res.country',
        string='Country',
    )
    address_city = fields.Many2one(
        'res.country.state',
        string='State',
    )
    address_municipality = fields.Many2one(
        'res.country.state.municipality',
        string='Municipality'
    )
    address_parish = fields.Many2one(
        'res.country.state.municipality.parish',
        string='Parish'
    )
    address_zip = fields.Char(string='Postal Code')
    alternative_identification = fields.Boolean(
        string='Alternative IDs',
        help='Other types of identification, not the official PUID.'
        'Examples : Passport, foreign ID,..'
    )
    alternative_ids = fields.One2many(
        string='Alternative IDs',
        comodel_name='medical.person.alternative.identification',
        inverse_name='name',
        states={'invisible': 'alternative_identification'}
    )
    insurance = fields.One2many(
        string='Insurances',
        comodel_name='medical.insurance.plan',
        inverse_name='name',
        help="Insurance Plans associated to this partner"
    )
    internal_user = fields.Many2one(
        string='Internal User',
        comodel_name='res.users',
        states={'invisible': 'is_person'},
        help='In GNU Health is the user (person) that logins.'
        'When the partner is a person, it will be the user'
        'that maps the partner.',
    )
    insurance_company_type = fields.Selection(
        [
            ('state', 'State'),
            ('labour_union', 'Labour Union / Syndical'),
            ('private', 'Private'),
        ],
        string='Insurance Type',
        index=True
    )
    Domiciliary_Unit = fields.Many2one(
        string='DU',
        comodel_name='housing.du',
        help="Domiciliary Unit"
    )
    du_address = fields.Text(
        string='Main address',
        help="Main Address, based on the associated DU"
        'get_du_address'
    )
    birth_certificate = fields.Many2one(
        'medical.birth.certificate',
        string='Birth Certificate',
        readonly=True
    )
    deceased = fields.Boolean(
        string='Deceased',
        readonly=True,
        help='The information is updated from the Death Certificate',
        states={'invisible': 'deceased'}
    )
    dod = fields.Datetime(
        string='Date of Death',
        states={'invisible': 'deceased'}
    )
    death_certificate = fields.Many2one(
        'medical.death.certificate',
        string='Death Certificate',
        readonly=True
    )
    mother = fields.Many2one(
        'res.partner',
        string='Mother',
        help="Mother from the Birth Certificate"
        'get_mother'
    )
    father = fields.Many2one(
        'res.partner',
        string='Father',
        help="Father from the Birth Certificate"
        'get_father'
    )
    fed_country = fields.Char(
        string='Prefix',
        help="3-letter Country code"
        "in ISO 3166-1 alpha-3 standard that will become the prefix"
        "of the federation account. The following user-assigned codes"
        "ranges can be also used"
        "AAA to AAZ, QMA to QZZ, XAA to XZZ, and ZZA to ZZZ."
        "For example XXX is unidentified nationality and XXB is a refugee."
        "By default, it will use the code of the emiting institution country"
        "Refer to the GNU Health manual for further information",
        states={'invisible': 'is_person'}
    )

    def get_mother(self, name):
        if (self.birth_certificate and self.birth_certificate.mother):
            return self.birth_certificate.mother.id

    def get_father(self, name):
        if (self.birth_certificate and self.birth_certificate.father):
            return self.birth_certificate.father.id

    def get_dod(self, name):
        if (self.deceased and self.death_certificate):
            return self.death_certificate.dod

    def generate_puid(self):
        # Add a default random string in the ref field.
        # The STRSIZE constant provides the length of the PUID
        # The format of the PUID is XXXNNNXXX
        # By default, this field will be used only if nothing is entered
        STRSIZE = 9
        puid = ''
        for x in range(STRSIZE):
            if (x < 3 or x > 5):
                puid = puid + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                puid = puid + random.choice("0123456789")
        return puid

    # def write(self, vals):
    #     actions = iter(vals)
    #     args = []
    #     for parties, vals in zip(actions, actions):
    #         given_name = family_name = ''
    #         vals = vals.copy()
    #         person_id = parties[0].id
    #         if vals.get('ref') == '':
    #             vals['ref'] = None
    #         if ('name' in vals) or ('lastname' in vals):
    #             given_name = family_name = ''
    #             if 'name' in vals:
    #                 given_name = vals['name']
    #             if 'lastname' in vals:
    #                 family_name = vals['lastname']
    #             if parties[0].is_person:
    #                 self.update_person_official_name(
    #                     person_id, given_name, family_name
    #                 )
    #         args.append(parties)
    #         args.append(vals)
    #     return super(ResPartner, self).write(vals)

    def update_person_official_name(self, person_id, given_name, family_name):
        # Create or update the official PersonName entry with the
        # Given / Family names from the main entry field.
        person = []
        Pname = self.env['medical.person.name']
        officialnames = Pname.search(
            [("partner_id", "=", person_id), ("use", "=", 'official')],)
        # If no official name found, create a new record
        if not (officialnames):
            values = {
                'partner_id': person_id,
                'use': 'official',
            }
            if given_name:
                values['given'] = given_name
            if family_name:
                values['family'] = family_name
            person.append(values)
            Pname.create(person)
        # Found a related official name record, then
        # update official Person Name(s) when modified in main form
        else:
            official_rec = []
            official_rec.append(officialnames[0])
            values = {'use': 'official'}
            if given_name:
                values['given'] = given_name
            if family_name:
                values['family'] = family_name
            Pname.write(official_rec, values)

    @api.model
    def create(self, vals):
        # Configuration = self.env['partner.configuration']
        vals = [x.copy() for x in vals]
        tmp_act = self.generate_puid()
        for values in vals:
            if not values.get('ref'):
                if values.get('federation_account'):
                    # Strip the country code from the fed account
                    # and pass it to the local PUID
                    values['ref'] = values.get('federation_account')[3:]
                else:
                    values['ref'] = tmp_act
                if 'unidentified' in values and values['unidentified']:
                    values['ref'] = 'NN-' + values.get('ref')
                if 'is_person' in values and not values['is_person']:
                    values['ref'] = 'NP-' + values['ref']
            # Generate the Federation account ID
            # with the ISO 3166-1 alpha-3 as prefix
            # using the same code as in the newly created PUID
            # If the person is NN or there is no country assigned
            # use the prefix XXX
            if not values.get('federation_account') and\
               values.get('is_person'):
                federation_account = tmp_act
                values['federation_account'] = \
                    values['fed_country'] + federation_account
            # Set the value to None to make the fields that have a
            # unique constraint get the NULL value at PostgreSQL level, and not
            # the value '' coming from the client
            if values.get('federation_account') == '':
                values['federation_account'] = None
            # Generate internal code
            # if not values.get('code'):
            #     config = Configuration(1)
                # Use the company name . Initially, use the name
                # since the company hasn't been created yet.
                # suffix = Transaction().context.get('company.rec_name') \
                #     or values['name']
                # Generate the partner code in the form of
                # "UUID-" . Where company is the name of the Health
                # Institution.
                #
                # The field "code" is the one that is used in distributed
                # environments, with multiple GNU Health instances across
                # a country / region
                # values['code'] = '%s-%s' % (uuid4(), suffix)
            values.setdefault('addresses', None)
            # If the partner is a physical person,
            # add new PersonName record with the given and family name
            # as the official name
            if (values.get('is_person')):
                if ('name' in values) or ('lastname' in values):
                    official_name = []
                    given_name = family_name = ''
                    if 'name' in values:
                        given_name = values['name']
                    if 'lastname' in values:
                        family_name = values['lastname']
                    official_name.append(('create', [{
                        'use': 'official',
                        'given': given_name,
                        'family': family_name,
                    }]))
                    values['person_names'] = official_name
        return super(ResPartner, self).create(vals)

    def get_rec_name(self, name):
        # Display name on the following sequence
        # 1 - Oficial Name from PersonName with the name representation
        # If not offficial name :
        # 2 - Last name, First name
        if self.person_names:
            prefix = given = family = suffix = ''
            for pname in self.person_names:
                if pname.prefix:
                    prefix = pname.prefix + ' '
                if pname.suffix:
                    suffix = ', ' + pname.suffix
                given = pname.given or ''
                family = pname.family or ''
                res = ''
                if pname.use == 'official':
                    if self.name_representation == 'pgfs':
                        res = prefix + given + ' ' + family + suffix
                    if self.name_representation == 'gf':
                        if pname.family:
                            family = ' ' + pname.family
                        res = given + family
                    if self.name_representation == 'fg':
                        if pname.family:
                            family = pname.family + ', '
                        res = family + given
                    if self.name_representation == 'cjk':
                        if pname.family:
                            family = pname.family
                        res = family + given
                    if not self.name_representation:
                        # Default value
                        if family:
                            return family + ', ' + given
                        else:
                            return given
                return res
        if self.lastname:
            return self.lastname + ', ' + self.name
        else:
            return self.name

    def search_rec_name(self, name, clause):
        """ Search for the name, lastname, PUID, any alternative IDs,
            and any family and / or given name from the person_names. """
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [
            bool_op,
            ('ref',) + tuple(clause[1:]),
            ('alternative_ids.code',) + tuple(clause[1:]),
            ('federation_account',) + tuple(clause[1:]),
            ('contact_mechanisms.value',) + tuple(clause[1:]),
            ('person_names.family',) + tuple(clause[1:]),
            ('person_names.given',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ('lastname',) + tuple(clause[1:]),
        ]

    @api.depends('is_person', 'is_patient', 'is_healthprof')
    def on_change_with_is_person(self):
        # Set is_person if the partner is a health professional or a patient
        if (self.is_healthprof or self.is_patient or self.is_person):
            return True

    @api.depends('du')
    def on_change_with_du_address(self):
        if (self.du):
            return self.get_du_address(name=None)

    def validate(self, parts):
        super(ResPartner, self).validate(parts)
        for partner in parts:
            partner.check_person()
            partner.validate_official_name()
            partner.validate_dob()

    def validate_dob(self):
        """ Check that the date is sane
                * The person is alive
                * Non-negative years, months or days
                * < 200 (future generations :) )"""
        if (self.dob):
            years, months, days = \
                self.compute_age_from_dates(
                    self.dob, self.deceased, self.dod, self.gender, 'raw_age',
                    None
                )
            if (not self.deceased):
                if (years < 0 or months < 0 or days < 0) or years > 200:
                    self.raise_user_error(
                        "Wrong date of birth for a living person"
                    )

    def check_person(self):
        # Verify that health professional and patient
        # are unchecked when is_person is False
        if not self.is_person and (self.is_patient or self.is_healthprof):
            self.raise_user_error(
                "The Person field must be set if the partner is a health"
                " professional or a patient"
            )

    def validate_official_name(self):
        # Only allow one official name on the partner name
        Pname = self.env['medical.person.name']
        officialnames = Pname.search_count(
            [("partner_id", "=", self.id), ("use", "=", 'official')]
        )
        if (officialnames > 1):
            self.raise_user_error("The person can have only one official name")

    def view_attributes(self):
        # Hide the group holding all the demographics when the partner is not
        # a person
        return super(ResPartner, self).view_attributes() + [
            (
                '//group[@id="person_details"]', 'states', {
                    'invisible': 'is_person',
                }
            )
        ]
