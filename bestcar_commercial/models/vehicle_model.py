from odoo import models, fields


class VehicleModel(models.Model):
    _name = "vehicle.model"
    _description = "Vehicle Model"

    name = fields.Char(string="Model")
    brand_id = fields.Many2one(comodel_name="vehicle.brand", string="Manufacturer")
    type_id = fields.Many2one(comodel_name="vehicle.type", string="Type")
