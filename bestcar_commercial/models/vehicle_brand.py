from odoo import models, fields


class VehicleBrand(models.Model):
    _name = "vehicle.brand"
    _description = "Vehicle Brand"

    name = fields.Char(string="Manufacturer")

    logo = fields.Image(string="Logo", max_width=128, max_height=128)

    model_ids = fields.One2many("vehicle.model", "brand_id", string="Models")
