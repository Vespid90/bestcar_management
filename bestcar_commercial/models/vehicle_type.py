from odoo import models, fields, api

class VehicleType(models.Model):
    _name = "vehicle.type"
    _description = "Vehicle Type"

    name = fields.Char(string="Type")
