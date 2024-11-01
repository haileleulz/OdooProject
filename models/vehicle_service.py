from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleService(models.Model):
    _name = "vehicle.service"
    _description = "Type of service for vehicle"

    required_service = fields.Selection([
        ('service', 'Service'),
        ('maintenance', 'maintenance'),
        ('inspection', 'Inspection'),
    ], string='Required Service', required=True)

    service_type = fields.Selection([
        ('regular', 'Regular'),
        ('one_time', 'One Time')
    ], string='Type of Service')

    inspection_type = fields.Selection([
        ('safety', 'Safety Inspection'),
        ('emissions', 'Emissions Inspection'),
        ('pre_purchase', 'Pre-Purchase Inspection'),
        ('annual', 'Annual Inspection'),
        ('commercial', 'Commercial Vehicle Inspection'),
        ('specialized', 'Specialized Inspection'),
        ('regular', 'Regular'),
        ('one_time', 'One Time')
    ], string='Type of Inspection')

    maintenance_type = fields.Selection([
        ('part_change', 'Part Change'),
        ('repair', 'Repair'),
        ('dismantle', 'Dismantle')
    ], string='Type of Maintenance')

    replacement_part_id = fields.Many2one('vehicle.parts', string="Replacement Part")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    cost_services = fields.Float(string="Payment for Services", compute="_compute_total_service_costs", default=15000)
    cost_maintenance = fields.Float(string="Payment for Maintenance", compute="_compute_cost_maintenance")
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge", default=0.0)
    discount = fields.Float(string="Discount", help="For being a regular customer", default=0.0)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation")
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id")
    date_registered = fields.Date(string="Date Registered", default=fields.Date.context_today)

    @api.depends("service_type")
    def _compute_total_service_costs(self):
        for rec in self:
            if rec.service_type:
                if rec.service_type == 'regular':
                    rec.cost_services = 15000 + rec.service_charge - rec.discount
                elif rec.service_type == 'one_time':
                    rec.cost_services = 15000 + rec.service_charge
                else:
                    rec.cost_services = 0.0

    @api.depends("maintenance_type")
    def _compute_cost_maintenance(self):
        for rec in self:
            if rec.maintenance_type:
                if rec.maintenance_type == 'part_change':
                    rec.cost_maintenance = rec.replacement_part_id.cost + rec.service_charge
                elif rec.maintenance_type == 'repair':
                    rec.cost_maintenance = rec.service_charge
                elif rec.maintenance_type == 'dismantle':
                    rec.cost_maintenance = rec.service_charge
                else:
                    rec.cost_maintenance = 0.0

    @api.depends("cost_services", "required_service", "cost_maintenance")
    def _compute_service_charge(self):
        for rec in self:
            if rec.required_service == 'inspection':
                rec.service_charge = 20000
            elif rec.required_service == 'service':
                rec.service_charge = rec.cost_services * 0.125
            elif rec.required_service == 'maintenance':
                if rec.cost_maintenance == 'part_change':
                    rec.service_charge = rec.cost_maintenance * 0.25
                if rec.cost_maintenance == 'repair':
                    rec.service_charge = rec.cost_maintenance * 0.35
                if rec.cost_maintenance == 'dismantle':
                    rec.service_charge = rec.cost_maintenance * 0.75
            else:
                rec.service_charge = 0.0

    @api.onchange("service_type")
    def _compute_discount(self):
        for rec in self:
            if rec.service_type == 'regular':
                rec.discount = 1000
            else:
                rec.discount = 0

    @api.depends("cost_services", "cost_maintenance")
    def _compute_taxation(self):
        for rec in self:
            rec.taxation = (rec.cost_services + rec.cost_maintenance) * 0.125

    @api.depends("cost_services", "cost_maintenance", "taxation")
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.cost_services + rec.cost_maintenance + rec.taxation
