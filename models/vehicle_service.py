from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleService(models.Model):
    _name = "vehicle.service"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Vehicle Service"
    # _rec_name =

    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel')
    ], default='new', string="Status")

    required_checkup_id = fields.Many2one('required.checkup', string='Required Service', required=True)
    service_type_id = fields.Many2one('service.type', string='Service Type')
    maintenance_type_id = fields.Many2one('maintenance.type', string='Maintenance Type')
    inspection_type_id = fields.Many2one('inspection.type', string='Inspection Type')
    replacement_part_id = fields.Many2one('vehicle.parts', string="Replacement Part")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    cost_services = fields.Float(string="Payment for Services", compute="_compute_total_service_costs")
    cost_maintenance = fields.Float(string="Payment for Maintenance", compute="_compute_cost_maintenance")
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge", default=0.0)
    discount = fields.Float(string="Discount", help="For being a regular customer", default=0.0)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation")
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id")
    date_registered = fields.Date(string="Date Registered", default=fields.Date.context_today)
    check = fields.Char(string="Check", compute="_compute_required_check", store=True)

    @api.onchange('required_checkup_id')
    def _compute_required_check(self):
        for rec in self:
            if rec.required_checkup_id:
                rec.check = rec.required_checkup_id.name
            else:
                rec.check = ''

    @api.depends("service_type_id")
    def _compute_total_service_costs(self):
        for rec in self:
            if rec.service_type_id == 'regular':
                rec.cost_services = 15000 + rec.service_charge - rec.discount
            elif rec.service_type_id == 'one_time':
                rec.cost_services = 15000 + rec.service_charge
            else:
                rec.cost_services = 0.0

    @api.depends("maintenance_type_id")
    def _compute_cost_maintenance(self):
        for rec in self:
            if rec.maintenance_type_id == 'part_change':
                rec.cost_maintenance = rec.replacement_part_id.cost + rec.service_charge
            elif rec.maintenance_type_id in ('repair', 'dismantle'):
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
                elif rec.cost_maintenance == 'repair':
                    rec.service_charge = rec.cost_maintenance * 0.35
                elif rec.cost_maintenance == 'dismantle':
                    rec.service_charge = rec.cost_maintenance * 0.75
                else:
                    rec.service_charge = 0.0
            else:
                rec.service_charge = 0.0

    @api.depends("service_type")
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
