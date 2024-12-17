from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleBrands(models.Model):
    _name = "vehicle.brands"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of vehicle brands"

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Html(string="Description", help="Please put the description of the car and its repair history")
    logo = fields.Binary(string='Logo', attachment=True)


class VehicleInformation(models.Model):
    _name = "vehicle.information"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Vehicle Information"

    # name = fields.Char(string="Name", compute="_compute_name")
    brand_id = fields.Many2one('vehicle.brands', string="Brand", store=True)

    color = fields.Char(string='Color')

    # color_mapping = {
    #     # Red shades
    #     "#FF5733": "Red",  # Dark Red
    #     "#FF6F61": "Red",  # Light Red
    #     "#800000": "Red",  # Burgundy
    #     "#FF0000": "Red",  # Pure Red
    #     "#FF6347": "Red",  # Tomato Red
    #     "#CD5C5C": "Red",  # Indian Red
    #     "#B22222": "Red",  # Firebrick
    #
    #     # Green shades
    #     "#33FF57": "Green",  # Lime Green
    #     "#228B22": "Green",  # Forest Green
    #     "#006400": "Green",  # Dark Green
    #     "#00FF00": "Green",  # Pure Green
    #     "#2E8B57": "Green",  # Sea Green
    #     "#32CD32": "Green",  # Lime
    #
    #     # Blue shades
    #     "#3357FF": "Blue",  # Medium Blue
    #     "#0000FF": "Blue",  # Pure Blue
    #     "#4682B4": "Blue",  # Steel Blue
    #     "#1E90FF": "Blue",  # Dodger Blue
    #     "#ADD8E6": "Blue",  # Light Blue
    #     "#5F9EA0": "Blue",  # Cadet Blue
    #
    #     # Yellow shades
    #     "#FFFF33": "Yellow",  # Yellow
    #     "#FFD700": "Yellow",  # Gold
    #     "#F0E68C": "Yellow",  # Khaki
    #     "#FFFACD": "Yellow",  # Lemon Chiffon
    #     "#FFE4B5": "Yellow",  # Moccasin
    #
    #     # Orange shades
    #     "#FFA500": "Orange",  # Orange
    #     "#FF8C00": "Orange",  # Dark Orange
    #     "#FF7F50": "Orange",  # Coral
    #     "#FF6347": "Orange",  # Tomato
    #
    #     # Purple shades
    #     "#800080": "Purple",  # Purple
    #     "#8A2BE2": "Purple",  # Blue Violet
    #     "#9370DB": "Purple",  # Medium Purple
    #     "#BA55D3": "Purple",  # Medium Orchid
    #     "#D8BFD8": "Purple",  # Thistle
    #
    #     # Pink shades
    #     "#FFC0CB": "Pink",  # Pink
    #     "#FF69B4": "Pink",  # Hot Pink
    #     "#FF1493": "Pink",  # Deep Pink
    #     "#DB7093": "Pink",  # Pale Violet Red
    #
    #     # Brown shades
    #     "#A52A2A": "Brown",  # Brown
    #     "#8B4513": "Brown",  # Saddle Brown
    #     "#D2691E": "Brown",  # Chocolate
    #     "#CD853F": "Brown",  # Peru
    #     "#F4A460": "Brown",  # Sandy Brown
    #
    #     # Gray shades
    #     "#808080": "Gray",  # Gray
    #     "#D3D3D3": "Gray",  # Light Gray
    #     "#A9A9A9": "Gray",  # Dark Gray
    #     "#C0C0C0": "Gray",  # Silver
    #     "#696969": "Gray",  # Dim Gray
    #
    #     # Black and White
    #     "#000000": "Black",  # Black
    #     "#FFFFFF": "White",  # White
    #     "#F5F5F5": "White",  # White Smoke
    #
    #     # Other colors
    #     "#800000": "Maroon",  # Maroon
    #     "#008080": "Teal",  # Teal
    #     "#DCDCDC": "Gainsboro",  # Gainsboro
    #     "#F0F8FF": "Alice Blue",  # Alice Blue
    # }
    #
    # @api.depends('color')
    # def _compute_color_name(self):
    #     for record in self:
    #         record.color_name = self.color_mapping.get(record.color, "Unknown Color")
    #
    # color_name = fields.Char(string="Color Name", compute="_compute_color_name", store=True)

    engine_cc = fields.Selection([
        ('800', '800 cc - Small Car'),
        ('1000_1500', '1000-1500 cc - Economy Car'),
        ('1600_2000', '1600-2000 cc - Standard SUV'),
        ('2000_3000', '2000-3000 cc - Mid-size SUV'),
        ('3000_up', '3000 cc and above - High SUV')
    ],
        string="Engine CC Type", help="Select the engine size category.")

    chassis = fields.Char(string='Chassis', required=True)
    license = fields.Char(string='License Plate', required=True)
    service_id = fields.Many2one('vehicle.service', string="Service")

    @api.depends('brand_id', 'license')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.brand_id.name} - {rec.license}"


class VehicleTags(models.Model):
    _name = "vehicle.tag"
    _description = "Property Tag"

    name = fields.Char(string='Name', required=True)
