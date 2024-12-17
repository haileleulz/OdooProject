from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleService(models.Model):
    _name = "vehicle.service"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Vehicle Service"
    _rec_name = 'required_checkup_id'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('request', 'Offer Requested'),
        ('accepted', 'Offer Accepted'),
        ('under_checkup', 'Under Checkup'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], default='new', string="Status")

    required_checkup_id = fields.Many2one('required.checkup', string='Required Service', required=True, store=True)
    service_type_id = fields.Many2one('service.type', string='Service Type', store=True)
    maintenance_type_id = fields.Many2one('maintenance.type', string='Maintenance Type', store=True)
    inspection_type_id = fields.Many2one('inspection.type', string='Inspection Type', store=True)
    replacement_part_ids = fields.Many2many('vehicle.parts', string="Replacement Part", store=True)
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
    tag_ids = fields.Many2many('vehicle.tag', string='Vehicle Tag')
    stock = fields.Integer(string="Stock", compute="_compute_stock", store=True)

    @api.depends('replacement_part_ids')
    def _compute_stock(self):
        for rec in self:
            total_stock = 0
            for part in rec.replacement_part_ids:
                total_stock = part.stock
            rec.stock = total_stock

    @api.onchange('replacement_part_ids')
    def _onchange_replacement_parts(self):
        if self.maintenance_type_id.name == 'Part Change':
            for rec in self.replacement_part_ids:
                if rec.stock > 0:
                    rec.stock -= 1
                    rec._origin.stock = rec.stock
                else:
                    raise ValidationError(_("The part %s is out of stock!") % rec.name)
        else:
            pass

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
                rec.name = 'Unnamed Service'

    @api.depends('service_type_id', 'replacement_part_ids', 'inspection_type_id')
    def _compute_cost(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.cost = rec.service_type_id.cost
                elif rec.replacement_part_ids:
                    total_cost = sum(part.cost for part in rec.replacement_part_ids)
                    rec.cost = total_cost
                elif rec.inspection_type_id:
                    rec.cost = rec.inspection_type_id.cost
                else:
                    rec.cost = 0.0
            else:
                rec.cost = 0.0

    @api.depends('service_type_id', 'replacement_part_ids', 'inspection_type_id')
    def _compute_service_charge(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.service_charge = rec.service_type_id.service_charge
                elif rec.replacement_part_ids:
                    total_service_charge = sum(part.service_charge for part in rec.replacement_part_ids)
                    rec.service_charge = total_service_charge
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

    @api.depends("maintenance_type_id", "replacement_part_ids.cost_maintenance", "replacement_part_ids")
    def _compute_cost_maintenance(self):
        for rec in self:
            if rec.maintenance_type_id:
                total_cost = 0.0
                for part in rec.replacement_part_ids:
                    total_cost = total_cost + part.cost_maintenance
                rec.cost_maintenance = total_cost
            else:
                rec.cost_maintenance = 0.0

    @api.depends('cost_services', 'cost_maintenance', 'cost_inspection', 'replacement_part_ids')
    def _compute_taxation(self):
        for rec in self:
            if rec.required_checkup_id:
                if rec.service_type_id:
                    rec.taxation = rec.service_type_id.taxation
                elif rec.replacement_part_ids:
                    rec.taxation = sum(part.taxation for part in rec.replacement_part_ids)
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

    # @api.constrains('driver_ids')
    # def _check_driver_information(self):
    #     for rec in self:
    #         if not rec.driver_ids:
    #             if len(rec.driver_ids.name) <= 2:
    #                 raise ValidationError(_("Please Enter The Driver Information."))
    #         if len(rec.driver_ids) > 1:
    #             raise ValidationError(_("Only one driver can be registered for a vehicle service."))

    @api.constrains('driver_ids')
    def _check_driver_information(self):
        for rec in self:
            if len(rec.driver_ids.name) <= 2:
                raise ValidationError(_("Please Enter The Driver Information."))
            if len(rec.driver_ids) > 1:
                raise ValidationError(_("Only one driver can be registered for a vehicle service."))

    @api.constrains('brand_ids')
    def _check_car_information(self):
        for rec in self:
            if not rec.brand_ids:
                raise ValidationError(_("Please Enter The Car Information."))

    def action_request(self):
        self.state = 'request'

    def action_accepted(self):
        self.state = 'cancel'

    def action_under_checkup(self):
        self.state = 'request'

    def action_done(self):
        self.state = 'cancel'

    def action_cancel(self):
        self.state = 'cancel'

    def _get_report_base_filename(self):
        self.ensure_one()
        if not self.name:
            self._compute_name()
        return 'Vehicle Service - %s' % self.name

    # @api.model
    # def create(self, vals):
    #     driver_name = vals.get('driver_ids')
    #     if driver_name:
    #         existing_driver = self.env['driver.information'].search([
    #             ('name', '=', vals.get('name')),
    #             ('gender', '=', vals.get('gender')),
    #             ('dob', '=', vals.get('dob')),
    #         ], limit=1)
    #         if existing_driver:
    #             vals['driver_ids'] = existing_driver.id
    #     return super(VehicleService, self).create(vals)
