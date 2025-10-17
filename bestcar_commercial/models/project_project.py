from odoo import models, fields


class Project(models.Model):
    _inherit = "project.project"

    vehicle_id = fields.Many2one(comodel_name="product.template", string="Vehicle")

    def action_view_vehicle(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Vehicle",
            "res_model": "product.template",
            "view_mode": "form",
            "res_id": self.vehicle_id.id,
        }
