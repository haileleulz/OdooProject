from odoo import http
from odoo.http import request


class PropertyController(http.Controller):
    @http.route(['/test/vehicle'], type='http', website=True, auth="public")
    def show_properties(self):
        # Fetch all records for vehicle brands and parts
        brands = request.env['vehicle.brands'].search([])
        parts = request.env['vehicle.parts'].search([])

        # Pass both sets of records to the template
        return request.render("test_vehicle.vehicles_page", {
            "brands": brands,
            "parts": parts
        })
