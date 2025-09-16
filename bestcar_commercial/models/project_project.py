from odoo import models, fields, api

class Project(models.Model):
    _inherit = "project.project"

    vehicle_id = fields.Many2one(comodel_name="product.template", string="Vehicle")