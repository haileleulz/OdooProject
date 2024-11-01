from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleParts(models.Model):
    _name = "vehicle.parts"
    # _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of vehicle parts"

    name = fields.Char(string="Name", required=True)
    cost = fields.Monetary(string="Cost", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
