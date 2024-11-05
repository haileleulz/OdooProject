from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleBrands(models.Model):
    _name = "vehicle.brands"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of vehicle brands"

    name = fields.Char(string="Name", required=True, tracking=True)
    description = fields.Html(string="Description", help="Please put the description of the car")
    logo = fields.Binary(string='Logo', attachment=True)
