from odoo import http
from odoo.http import request


class PropertyController(http.Controller):
    @http.route(['/test/vehicle'], type='http', website=True, auth="public")
    def show_properties(self):
        brands = request.env['vehicle.brands'].search([])
        parts = request.env['vehicle.parts'].search([])

        return request.render("test_vehicle.vehicles_page", {
            "brands": brands,
            "parts": parts
        })

