from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleBrands(models.Model):
    _name = "vehicle.brands"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of vehicle brands"

    name = fields.Char(string="Name", required=True)
    # image = fields.Image(string="Logo")
    # logo = fields.Binary(string='Logo', attachment=True)
