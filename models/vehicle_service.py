from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleService(models.Model):
    _name = "vehicle.service"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Vehicle Service"
    _rec_name = 'required_checkup_id'
    # _rec_name = 'name'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('request', 'Offer Request'),
        ('accepted', 'Offer Accepted'),
        ('declined', 'Offer Declined'),
        ('under_checkup', 'Under Checkup'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='new', string="Status")

    required_checkup_id = fields.Many2one('required.checkup', string='Required Service', required=True, store=True)
    service_type_id = fields.Many2one('service.type', string='Service Type', store=True)
    maintenance_type_id = fields.Many2one('maintenance.type', string='Maintenance Type', store=True)
    inspection_type_id = fields.Many2one('inspection.type', string='Inspection Type', store=True)
    replacement_part_id = fields.Many2many('vehicle.parts', string="Replacement Part", store=True)
    discount = fields.Float(string="Discount", compute="_compute_discount", store=True)
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    cost_services = fields.Float(string="Payment for Services", compute="_compute_cost_service", store=True)
    cost_maintenance = fields.Float(string="Payment for Maintenance", compute="_compute_cost_maintenance", store=True)
    cost_inspection = fields.Float(string="Payment for Inspection", compute="_compute_cost_inspection", store=True)
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge", compute="_compute_service_charge",
                                  store=True)
    cost = fields.Float(string="Items Cost", help="Cost of items and services", compute="_compute_cost", store=True)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation", store=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id",
                                 store=True)
    date_registered = fields.Date(string="Date Registered", default=fields.Date.context_today)
    appointment_date = fields.Date(string="Date Of Appointment", required=True)
    driver_ids = fields.One2many('driver.information', 'vehicle_id', string="Personal Information", required=True)
    brand_ids = fields.One2many('vehicle.information', 'service_id', string="Vehicle Information", required=True)
    check = fields.Char(string="Check", compute="_compute_required_check", store=True)
    details = fields.Boolean(string="Payment Details")
    suggestion = fields.Html(string="Suggestion")

    @api.depends('required_checkup_id')
    def _compute_required_check(self):
        for rec in self:
            if rec.required_checkup_id:
                rec.check = rec.required_checkup_id.name
            else:
                rec.check = ''

    @api.depends('required_checkup_id', 'service_type_id')
    def _compute_discount(self):
        for rec in self:
            if not rec.service_type_id:
                rec.discount = 0
            else:
                rec.discount = rec.service_type_id.discount

    @api.onchange('required_checkup_id', 'service_type_id', 'inspection_type_id', 'maintenance_type_id')
    def _compute_name(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.name = f"{rec.required_checkup_id.name} - {rec.service_type_id.name}"
                elif rec.inspection_type_id:
                    rec.name = f"{rec.required_checkup_id.name} - {rec.inspection_type_id.name}"
                elif rec.maintenance_type_id:
                    rec.name = f"{rec.required_checkup_id.name} - {rec.maintenance_type_id.name}"
                else:
                    rec.name = rec.required_checkup_id.name
            else:
                rec.name = ''

    @api.depends('service_type_id', 'maintenance_type_id', 'inspection_type_id')
    def _compute_cost(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.cost = rec.service_type_id.cost
                elif rec.maintenance_type_id:
                    rec.cost = rec.maintenance_type_id.cost
                elif rec.inspection_type_id:
                    rec.cost = rec.inspection_type_id.cost
                else:
                    rec.cost = 0.0
            else:
                rec.cost = 0.0

    @api.depends('service_type_id', 'maintenance_type_id', 'inspection_type_id')
    def _compute_service_charge(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.service_charge = rec.service_type_id.service_charge
                elif rec.maintenance_type_id:
                    rec.service_charge = rec.maintenance_type_id.service_charge
                elif rec.inspection_type_id:
                    rec.service_charge = rec.inspection_type_id.service_charge
                else:
                    rec.service_charge = 0.0
            else:
                rec.cost = 0.0

    @api.depends('inspection_type_id', 'required_checkup_id')
    def _compute_cost_inspection(self):
        for rec in self:
            if rec.required_checkup_id and rec.inspection_type_id:
                rec.cost_inspection = rec.inspection_type_id.cost_inspection
            else:
                rec.cost_inspection = 0.0

    @api.depends('service_type_id', 'required_checkup_id')
    def _compute_cost_service(self):
        for rec in self:
            if rec.required_checkup_id and rec.service_type_id:
                rec.cost_services = rec.service_type_id.cost_services - rec.discount
            else:
                rec.cost_services = 0.0

    @api.depends("maintenance_type_id", 'replacement_part_id')
    def _compute_cost_maintenance(self):
        for rec in self:
            if rec.maintenance_type_id and rec.replacement_part_id:
                if rec.maintenance_type_id.name == 'part_change':
                    rec.cost_maintenance = rec.replacement_part_id.cost + rec.maintenance_type_id.service_charge
                elif rec.maintenance_type_id.name in ('repair', 'dismantle'):
                    rec.cost_maintenance = rec.service_charge
                else:
                    rec.cost_maintenance = 0.0
            else:
                rec.cost_maintenance = 0.0

    @api.depends('cost_services', 'cost_maintenance', 'cost_inspection', 'replacement_part_id')
    def _compute_taxation(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.taxation = rec.service_type_id.taxation
                elif rec.maintenance_type_id:
                    rec.taxation = rec.maintenance_type_id.taxation
                elif rec.inspection_type_id:
                    rec.taxation = rec.inspection_type_id.taxation
                else:
                    rec.taxation = 0.0
            else:
                rec.taxation = 0.0

    @api.depends('cost_services', 'cost_maintenance', 'cost_inspection', 'taxation')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.cost_services + rec.cost_maintenance + rec.cost_inspection + rec.taxation

    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for rec in self:
            if rec.appointment_date and rec.date_registered:
                if rec.appointment_date - rec.date_registered < timedelta(days=5):
                    raise ValidationError(_("Please make appointments at least 5 days in advance"))

    @api.constrains('driver_ids')
    def _check_single_driver(self):
        for rec in self:
            if len(rec.driver_ids) > 1:
                raise ValidationError(_("Only one driver can be registered for a vehicle service."))

    @api.constrains('driver_ids')
    def _check_driver_information(self):
        for rec in self:
            if not rec.driver_ids:
                raise ValidationError(_("Please Enter The Driver Information."))

    @api.constrains('brand_ids')
    def _check_car_information(self):
        for rec in self:
            if not rec.brand_ids:
                raise ValidationError(_("Please Enter The Car Information."))
