# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, models, fields
from odoo.modules import get_module_resource


class MedicalCenter(models.Model):
    _name = 'medical.center'
    _description = 'Medical Center'
    _inherit = 'medical.abstract.entity'

    is_institution = fields.Boolean(
        string='Institution',
        help='Check if the partner is a Health Care Institution'
    )

    @api.model
    def _create_vals(self, vals):
        vals.update({
            'is_company': True,
            # 'customer': False,
        })
        return super(MedicalCenter, self)._create_vals(vals)

    def _get_default_image_path(self, vals):
        super(MedicalCenter, self)._get_default_image_path(vals)
        return get_module_resource(
            'medical_center', 'static/src/img', 'medical-center-avatar.png',
        )


# Ported from GnuHealth
# class OperationalSector(models.Model):
#     _name = 'operational.sector'
#     _description = 'Operational Sector'
#
#     name = fields.Char(
#         'Op. Sector', required=True,
#         help='Region included in an operational area')
#     operational_area = fields.Many2one(
#         'operational.area', 'Operational Area')
#     info = fields.Text('Extra Information')
#
#     _sql_constraints = [
#         (
#             'operational_area_name_uniq',
#             'unique(name, operational_area)',
#             'The operational sector must be unique in each operational area!'
#         )
#     ]


class HealthInstitution(models.Model):
    _name = 'institution'
    _description = 'Health Institution'

    name = fields.Many2one(
        'medical.center',
        'Institution',
        help='Partner associated with this institution',
    )
    code = fields.Char(
        'Code',
        required=True
    )
    picture = fields.Binary('Picture')
    institution_type = fields.Selection(
        [
            ('doctor_office', 'Doctor office'),
            ('primary_care', 'Primary care center'),
            ('clinic', 'Clinic'),
            ('hospital', 'General Hospital'),
            ('specialized', 'Specialized Hospital'),
            ('nursing_home', 'Nursing home'),
            ('hospice', 'Hospice'),
            ('rural', 'Rural instalation'),
            ('pasi', 'PASI'),
            ('cat', 'CAT'),
            ('cdi', 'CDI'),
        ],
        'Type',
        required=True,
        sort=False
    )
    beds = fields.Integer("Beds")
    operating_room = fields.Boolean(
        "Operating room",
        help="Does the institution have an operating room?",
    )
    or_number = fields.Integer("Operating rooms")
    public_level = fields.Selection(
        [
            ('private', 'Private'),
            ('public', 'Public'),
            ('mixed', 'Mixed'),
        ],
        'Public level',
        required=True,
        sort=False
    )
    teaching = fields.Boolean(
        "Teaching",
        help="Is it a teaching institution?"
    )
    heliport = fields.Boolean("Heliport")
    trauma_center = fields.Boolean("Trauma center")
    trauma_level = fields.Selection(
        [
            ('I', 'Level I'),
            ('II', 'Level II'),
            ('III', 'Level III'),
            ('IV', 'Level IV'),
            ('V', 'Level V'),
        ],
        'Trauma level',
        sort=False
    )
    extra_info = fields.Text("Additional information")
    specialties = fields.One2many(
        'institution.specialties',
        'name',
        'Specialties',
        help="Specialties Provided in this Health Institution"
    )
    main_specialty = fields.Many2one(
        'institution.specialties',
        'Specialty',
        help="Main specialty, for specialized hospitals",
    )
    operational_sectors = fields.One2many(
        'institution.operationalsector',
        'name',
        'Operational Sector',
        help="Operational Sectors covered by this institution"
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'This institution exists'
        ), (
            'code_uniq',
            'unique(code)',
            'This code exists'
        )
    ]


class HealthInstitutionSpecialties(models.Model):
    _name = 'institution.specialties'
    _description = 'Health Institution Specialties'

    name = fields.Many2one(
        'institution',
        'Institution',
        required=True
    )
    specialty = fields.Many2one(
        'medical.specialty',
        'Specialty',
        required=True
    )

    _sql_constraints = [
        (
            'name_sp_uniq',
            'unique(name, specialty)',
            'This specialty exists for this institution'
        )
    ]

    def get_rec_name(self, name):
        if self.specialty:
            return self.specialty.name


class HealthInstitutionOperationalSector(models.Model):
    _name = 'institution.operationalsector'
    _description = 'Operational Sectors covered by this institution'

    name = fields.Many2one(
        'institution',
        'Institution',
        required=True
    )
    # operational_sector = fields.Many2one(
    #     'operational.sector',
    #     'Operational Sector',
    #     required=True
    # )


class Building(models.Model):
    _name = 'building'
    _description = 'Hospital Building'

    name = fields.Char(
        'Name',
        required=True,
        help='Name of the building within the institution'
    )
    institution = fields.Many2one(
        'institution',
        'Institution',
        required=True,
        help='Health Institution of this building'
    )
    code = fields.Char('Code', required=True)
    extra_info = fields.Text('Additiona information')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name, institution)',
            'The building name must be unique'
        ), (
            'code_uniq',
            'unique(code, institution)',
            'The building code must be unique'
        )
    ]

    def default_institution():
        return HealthInstitution().get_institution()


class HospitalUnit(models.Model):
    _name = 'hospital.unit'
    _description = 'Hospital Unit'

    name = fields.Char(
        'Name',
        required=True,
        help='Name of the unit, eg. Neonatal, Intensive Care ...'
    )
    institution = fields.Many2one(
        'institution',
        'Institution',
        required=True,
        help='Health Institution'
    )
    code = fields.Char('Code', required=True)
    extra_info = fields.Text('Additional information')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name, institution)',
            'The Unit name must be unique'
        ), (
            'code_uniq',
            'unique(code, institution)',
            'The Unit code must be unique'
        )
    ]

    def default_institution():
        return HealthInstitution().get_institution()


class HospitalOR(models.Model):
    _name = 'hospital.or'
    _description = 'Operating Room'

    name = fields.Char(
        'Name',
        required=True,
        help='Operating room name'
    )
    institution = fields.Many2one(
        'institution',
        'Institution',
        required=True,
        help='Health Institution'
    )
    building = fields.Many2one(
        'building',
        'Building'
    )
    unit = fields.Many2one('hospital.unit', 'Unit')
    extra_info = fields.Text('Additional Info')
    state = fields.Selection(
        [
            ('free', 'Free'),
            ('confirmed', 'Confirmed'),
            ('occupied', 'Occupied'),
            ('na', 'Not available'),
        ],
        'Status',
        readonly=True,
        sort=False
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name, institution)',
            'This name exists for this unit'
        ),
    ]

    def default_institution():
        return HealthInstitution().get_institution()

    def default_state():
        return 'free'


class HospitalWard(models.Model):
    _name = 'hospital.ward'
    _description = 'Hospital Ward'

    name = fields.Char(
        'name',
        required=True,
        help='Ward name/code'
    )
    institution = fields.Many2one(
        'institution',
        'Institution',
        required=True
    )
    building = fields.Many2one(
        'building',
        'Building'
    )
    floor = fields.Integer('Floor number')
    unit = fields.Many2one('hospital.unit', 'Unit')
    private = fields.Boolean(
        'Private',
        help='Check this option for private room'
    )
    bio_hazard = fields.Boolean(
        'Bio Hazard',
        help='Check this option if there is biological hazard'
    )
    number_of_beds = fields.Integer(
        'Number of beds',
        help='Number of patients per ward'
    )
    telephone = fields.Boolean('Telephone access')
    ac = fields.Boolean('Air Conditioning')
    private_bathroom = fields.Boolean('Private Bathroom')
    guest_sofa = fields.Boolean('Guest sofa-bed')
    tv = fields.Boolean('Television')
    internet = fields.Boolean('Internet Access')
    refrigerator = fields.Boolean('Refrigerator')
    microwave = fields.Boolean('Microwave')
    gender = fields.Selection(
        [
            ('men', 'Men\'s ward'),
            ('women', 'Women\'s ward'),
            ('unisex', 'Unisex'),
        ],
        'Gender',
        required=True,
        sort=False
    )
    state = fields.Selection(
        [
            ('beds_available', 'Beds available'),
            ('full', 'Full'),
            ('na', 'Not available'),
        ],
        'Status',
        sort=False
    )
    extra_info = fields.Text('Inf. Extra')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name, institution)',
            'The Ward / Room Name must be unique'
        ),
    ]

    def default_gender():
        return 'unisex'

    def default_number_of_beds():
        return 1

    def default_institution():
        return HealthInstitution().get_institution()


class HospitalBed(models.Model):
    _name = 'hospital.bed'
    _rec_name = 'telephone_number'
    _description = 'Hospital Bed'

    name = fields.Many2one(
        'product.product',
        'Bed',
        required=True,
        domain=[('is_bed', '=', True)],
        help='Bed Number'
    )
    institution = fields.Many2one(
        'institution',
        'Institution',
        required=True,
        help='Health institution'
    )
    ward = fields.Many2one(
        'hospital.ward',
        'Ward'
    )
    bed_type = fields.Selection(
        [
            ('gatch', 'Gatch bed'),
            ('electric', 'Electric'),
            ('stretcher', 'Stretcher'),
            ('low', 'Low bed'),
            ('low_air_loss', 'Low air loss'),
            ('circo_electric', 'Circo Electric'),
            ('clinitron', 'Clinitron'),
        ],
        'Bed type',
        required=True,
        sort=False
    )
    telephone_number = fields.Char(
        'Phone number',
        help='Number/Extention'
    )
    extra_info = fields.Text('Additional information')
    state = fields.Selection(
        [
            ('free', 'free'),
            ('reserved', 'Reserved'),
            ('occupied', 'Occupied'),
            ('to_clean', 'To be cleaned'),
            ('na', 'Not available'),
        ],
        'State',
        readonly=True,
        sort=False
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name, institution)',
            'The bed must be unique'
        )
    ]

    def default_bed_type():
        return 'gatch'

    def default_state():
        return 'free'

    def default_institution():
        return HealthInstitution().get_institution()

    def get_rec_name(self, name):
        if self.name:
            return self.name.name

    def search_rec_name(self, name, clause):
        return [('name',) + tuple(clause[1:])]
