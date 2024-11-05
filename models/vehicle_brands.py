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

    name = fields.Char(string="Name", compute="_compute_name")
    brand_id = fields.Many2one('vehicle.brands', string="Brand", store=True)
    color = fields.Char(string='Color')
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
