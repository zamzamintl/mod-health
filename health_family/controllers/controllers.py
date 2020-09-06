# Copyright 2011-2020 GNU Solidario
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).


# from odoo import http


# class HealthFamily(http.Controller):
#     @http.route('/health_family/health_family/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/health_family/health_family/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('health_family.listing', {
#             'root': '/health_family/health_family',
#             'objects': http.request.env['health_family.health_family'].search([]),
#         })

#     @http.route('/health_family/health_family/objects/<model("health_family.health_family"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('health_family.object', {
#             'object': obj
#         })
