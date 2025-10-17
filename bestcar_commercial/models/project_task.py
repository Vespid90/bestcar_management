from odoo import models, fields


class Project(models.Model):
    _inherit = "project.task"

    vehicle_id = fields.Many2one(related="project_id.vehicle_id")

    def open_view_vehicle(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Vehicle",
            "res_model": "product.template",
            "view_mode": "form",
            "res_id": self.vehicle_id.id,
        }
