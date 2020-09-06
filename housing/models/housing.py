# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from collections import OrderedDict
from odoo import models, fields, api
from werkzeug import urls, url_encode


class DomiciliaryUnit(models.Model):
    _name = 'housing.du'
    _description = 'Domiciliary Unit'

    name = fields.Char('Code', required=True)
    desc = fields.Char('Description')
    address_street = fields.Char('Sreet')
    address_street_number = fields.Integer('Number')
    address_street_bis = fields.Char('Apartment', required=False)
    address_country = fields.Many2one(
        'res.country',
        'Country',
        domain=[('name', '=', 'Venezuela')]
    )
    address_city = fields.Many2one(
        'res.country.state',
        string='State',
        domain=[('name', '=', 'Zulia')]
    )
    address_municipality = fields.Many2one(
        'res.country.state.municipality',
        string='Municipality'
    )
    address_parish = fields.Many2one(
        'res.country.state.municipality.parish',
        string='Parish'
    )
    address_zip = fields.Char('Postal Code')
    # operational_sector = fields.Many2one(
    #     'gnuhealth.operational_sector', 'Operational Sector'
    # )
    # picture = fields.Binary('Picture')
    latitude = fields.Float('Latitude', digits=(3, 14))
    longitude = fields.Float('Longitude', digits=(4, 14))
    altitude = fields.Integer('Altitude', help="M.A.S.L.")
    urladdr = fields.Char(
        'OSM Map',
        help="Locates the DU on the Open Street Map by default"
    )
    # Text Representation
    # address_repr = fields.Text("DU Address")
    # Infrastructure
    dwelling = fields.Selection(
        [
            ('single_house', 'Individual / Independent'),
            ('apartment', 'Apartment'),
            ('townhouse', 'Townhouse'),
            ('annexed', 'Annexed'),
            ('habitacion', 'Room'),
            ('mobilehome', 'Trailer'),
        ],
        'Tipo',
        sort=False
    )
    materials = fields.Selection(
        [
            ('concrete', 'Concrete'),
            ('adobe', 'Adobe'),
            ('metal', 'Metal/tin'),
            ('wood', 'Wood'),
            ('mud', 'Mud'),
            ('stone', 'Stone'),
            ('otros', 'Others'),
        ],
        'Construction material',
        sort=False
    )
    roof_type = fields.Selection(
        [
            ('concrete', 'Concrete'),
            ('adobe', 'Adobe'),
            ('wood', 'Wood'),
            ('mud', 'Mud'),
            ('thatch', 'Thatch'),
            ('stone', 'Stone'),
            ('metal', 'Metal/tin'),
        ],
        'Tipo de techo',
        sort=False
    )
    total_surface = fields.Integer('Surface', help="Surface in meters")
    bedrooms = fields.Integer('Bedrooms')
    bathrooms = fields.Integer('Bathrooms')
    housing = fields.Selection(
        [
            ('0', 'Deficient'),
            ('1', 'Small in good conditions'),
            ('2', 'Buenas condiciones'),
            ('3', 'Good conditions'),
            ('4', 'Luxurious'),
        ],
        'conditions',
        help="Sanitary Information",
        sort=False
    )
    sewers = fields.Boolean('Has a sewer system')
    water = fields.Boolean('Has water service')
    trash = fields.Boolean('Garbage collection service')
    electricity = fields.Boolean('Has electricity')
    gas = fields.Boolean('Has gas service')
    telephone = fields.Boolean('Has telephone service')
    television = fields.Boolean('Has tv signal')
    internet = fields.Boolean('Has internet service')
    members = fields.One2many('res.partner', 'housing')
    full_address = fields.Text(
        'Address',
        readonly=True, compute="_full_address"
    )

    _sql_constraints = [(
        'code_uniq',
        'unique(name)',
        'El código debe ser único'
    )]

    def get_parent(self, subdivision):
        # Recursively get the parent subdivisions
        if (subdivision.parent):
            return str(subdivision.rec_name) + '\n' + \
                str(self.get_parent(subdivision.parent))
        else:
            return subdivision.rec_name

    def get_du_address(self, name):
        du_addr = ''
        # Street
        if (self.address_street):
            du_addr = str(self.address_street) + ' ' + \
                str(self.address_street_number) + "\n"
        # Grab the parent subdivisions
        if (self.address_subdivision):
            du_addr = du_addr + \
                str(self.get_parent(subdivision=self.address_subdivision))
        # Zip Code
        if (self.address_zip):
            du_addr = du_addr + " - " + self.address_zip
        # Country
        if (self.address_country):
            du_addr = du_addr + "\n" + self.address_country.rec_name
        return du_addr

    @api.depends(
        'latitude', 'longitude', 'address_street', 'address_street_number',
        'address_district', 'address_municipality', 'address_city',
        'address_zip', 'address_subdivision', 'address_country'
    )
    def _on_change_with_urladdr(self):
        # Generates the URL to be used in OpenStreetMap
        #   If latitude and longitude are known, use them.
        #   Otherwise, use street, municipality, city, and so on.
        parts = OrderedDict()
        parts['scheme'] = 'http'
        parts['netloc'] = ''
        parts['path'] = ''
        parts['params'] = ''
        parts['query'] = ''
        parts['fragment'] = ''

        if (self.latitude and self.longitude):
            parts['netloc'] = 'openstreetmap.org'
            parts['path'] = '/'
            parts['query'] = url_encode({
                'mlat': self.latitude, 'mlon': self.longitude
            })
        else:
            state = country = postalcode = city = municipality = street = \
                number = ''
            if self.address_street_number is not None:
                number = str(self.address_street_number)
            if self.address_street:
                street = self.address_street
            if self.address_municipality:
                municipality = self.address_municipality
            if self.address_city:
                city = self.address_city
            if self.address_zip:
                postalcode = self.address_zip
            if self.address_subdivision:
                state = self.address_subdivision.name
            if self.address_country:
                country = self.address_country.code

            parts['netloc'] = 'nominatim.openstreetmap.org'
            parts['path'] = 'search'
            parts['query'] = url_encode({
                'street': ' '.join([number, street]).strip(),
                'county': municipality,
                'city': city,
                'state': state,
                'postalcode': postalcode,
                'country': country
            })
        return urls.url_unparse(list(parts.values()))

    # Show the resulting Address representation in realtime
    @api.depends(
        'address_street', 'address_subdivision', 'address_street_number',
        'address_country'
    )
    def on_change_with_address_repr(self):
        return self.get_du_address(name=None)

    @api.depends(
        'address_street', 'address_street_number', 'address_street_bis',
        'address_city', 'address_country'
    )
    def _full_address(self):
        for record in self:
            record.full_address = '{0} {1} {2}, {3} - {4} '.format(
                record.address_street, record.address_street_number,
                record.address_street_bis, record.address_city.name,
                record.address_country.name
            )
