from odoo import http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route(['/test/vehicle'], type='http', website=True, auth="public")
    def show_properties(self):
        return request.render("test_vehicle.vehicles_page", {})
