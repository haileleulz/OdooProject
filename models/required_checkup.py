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
    cost = fields.Monetary(string="Cost", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    discount = fields.Float(string="Discount", help="For being a regular customer")
    # discount = fields.Float(string="Discount", help="For being a regular customer", compute="_compute_discount",
    #                         store=True)
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge")
    # service_charge = fields.Float(string="Service Charge", help="Handyman Charge", compute="_compute_service_charge",
    #                               store=True)
    cost_services = fields.Float(string="Payment for Services", compute="_compute_cost_service", store=True)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation", store=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id",
                                 store=True)

    @api.depends('name', 'service_charge', 'cost', 'discount')
    def _compute_cost_service(self):
        for rec in self:
            if rec.name in ['Regular Service', 'Full Service']:
                rec.cost_services = rec.service_charge + rec.cost
            elif rec.name in ['One Time Service', 'Half Service']:
                rec.cost_services = rec.service_charge + rec.cost
            else:
                rec.cost_services = 0.0

    @api.depends('cost_services')
    def _compute_taxation(self):
        for rec in self:
            if rec.name:
                rec.taxation = rec.cost_services * 0.125
            else:
                rec.taxation = 0.0

    @api.depends('cost_services', 'taxation', 'discount')
    def _compute_total_cost(self):
        for rec in self:
            if rec.name:
                rec.total_cost = (rec.cost_services + rec.taxation) - rec.discount
            else:
                rec.rec.total_cost = 0.0


class VehicleInspectionType(models.Model):
    _name = "inspection.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of inspection for vehicle"

    name = fields.Char(string='Name', required=True)
    cost = fields.Monetary(string="Cost", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge", compute="_compute_service_charge",
                                  store=True)
    cost_inspection = fields.Float(string="Payment for Services", compute="_compute_cost_inspection", store=True)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation", store=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id",
                                 store=True)

    @api.depends('name')
    def _compute_cost_inspection(self):
        for rec in self:
            if rec.name:
                rec.cost_inspection = rec.service_charge + rec.cost
            else:
                rec.cost_inspection = 0.0

    @api.depends('cost_inspection')
    def _compute_taxation(self):
        for rec in self:
            if rec.name:
                rec.taxation = rec.cost_inspection * 0.125
            else:
                rec.taxation = 0.0

    @api.depends('cost_inspection', 'taxation')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.cost_inspection + rec.taxation
