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

    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(_("Date of Birth not acceptable!!"))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('information.driver')
        return super(DriverInformation, self).create(vals)

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

    # _sql_constraints = [
    #     ('uniq_name', 'unique (name)', 'The name of the DRIVER must be unique!')]

