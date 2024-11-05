from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RequiredCheckup(models.Model):
    _name = "required.checkup"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of checkup required"

    name = fields.Char(string='Name', required=True)


class VehicleServiceType(models.Model):
    _name = "service.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of service for vehicle"

    name = fields.Char(string='Name', required=True)


class VehicleInspectionType(models.Model):
    _name = "inspection.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of inspection for vehicle"

    name = fields.Char(string='Name', required=True)


class VehicleMaintenanceType(models.Model):
    _name = "maintenance.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of maintenance for vehicle"

    name = fields.Char(string='Name', required=True)
