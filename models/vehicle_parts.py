from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleMaintenanceType(models.Model):
    _name = "maintenance.type"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of maintenance for vehicle"

    name = fields.Char(string="Name", required=True)


class VehicleParts(models.Model):
    _name = "vehicle.parts"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Type of vehicle parts"

    name = fields.Char(string="Name", required=True)
    maintenance_id = fields.Many2one('maintenance.type', string="Maintenance Type")
    image = fields.Image(string="Image")
    describe = fields.Html(string="Description", help="Please put the description of the parts")
    cost = fields.Monetary(string="Cost", required=True, currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency", required=True,
                                  default=lambda self: self.env.company.currency_id)
    service_charge = fields.Float(string="Service Charge", help="Handyman Charge", compute="_compute_service_charge",
                                  store=True)
    cost_maintenance = fields.Float(string="Payment for Services", compute="_compute_cost_maintenance", store=True)
    taxation = fields.Float(string="Taxation", compute="_compute_taxation", store=True)
    total_cost = fields.Monetary(string="Total Cost", compute="_compute_total_cost", currency_field="currency_id",
                                 store=True)
    stock = fields.Integer(string="Stock Quantity", help="Available stock for the vehicle part")

    @api.depends('cost')
    def _compute_service_charge(self):
        for rec in self:
            rec.service_charge = rec.cost * 0.35

    @api.depends('cost', 'service_charge', 'maintenance_id.name')
    def _compute_cost_maintenance(self):
        for rec in self:
            if rec.maintenance_id.name == "Part Change":
                rec.cost_maintenance = rec.service_charge + rec.cost
            else:
                rec.cost_maintenance = rec.service_charge

    @api.depends('cost_maintenance')
    def _compute_taxation(self):
        for rec in self:
            rec.taxation = rec.cost_maintenance * 0.125

    @api.depends('cost_maintenance', 'taxation')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.cost_maintenance + rec.taxation

    def update_stock(self, quantity):
        self.ensure_one()
        self.stock += quantity


class UpdateStockWizard(models.TransientModel):
    _name = "vehicle.stock.wizard"
    _description = "Wizard to Update Stock"

    part_id = fields.Many2one('vehicle.parts', string="Vehicle Part", required=True)
    update_qty = fields.Float(string="Update Quantity", required=True)
    current_stock = fields.Integer(related="part_id.stock", string="Current Stock", readonly=True)

    def action_update_stock(self):
        self.ensure_one()
        if self.part_id:
            if self.update_qty < 0:
                raise ValidationError(_("The quantity cannot be negative."))
            self.part_id.update_stock(self.update_qty)
