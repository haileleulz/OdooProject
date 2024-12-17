from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DriverInformation(models.Model):
    _name = "driver.information"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Information of the driver"

    name = fields.Char(string="Name", required=True)
    image = fields.Image(string="Image")
    ref = fields.Char(string="Reference", tracking=True, help="Reference of the accountant record")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    dob = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string='Age', compute="compute_age", store=True, tracking=True)
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single'), ('divorced', 'Divorced')],
                                      string="Marital Status", tracking=True, required=True)
    partner_name = fields.Char(string="Partner Name", tracking=True)
    vehicle_id = fields.Many2one('vehicle.service', string="Service")
    phone = fields.Char(string="Phone Number", required=True)
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Date of Birth not acceptable!!"))

    @api.model
    def create(self, vals):
        existing_driver = self.search([
            ('name', '=', vals.get('name')),
            ('gender', '=', vals.get('gender')),
            ('dob', '=', vals.get('dob')),
        ], limit=1)
        if existing_driver:
            vals['ref'] = existing_driver.ref
        else:
            vals['ref'] = self.env['ir.sequence'].next_by_code('information.driver')
        return super(DriverInformation, self).create(vals)

    def unlink(self):
        for rec in self:
            if rec.vehicle_id and rec.vehicle_id.state != 'new':
                raise ValidationError(_("You cannot delete this driver state because there is an ongoing transaction."))
        return super(DriverInformation, self).unlink()

    @api.depends("dob")
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                rec.age = today.year - rec.dob.year
            else:
                rec.age = 1

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age < 18:
                raise ValidationError("Designated driver must be at least 18!")

    def _get_report_base_filename(self):
        report = f"Driver_{self.name}"
        return report
