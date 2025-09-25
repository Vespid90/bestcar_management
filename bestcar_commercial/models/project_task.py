from odoo import models, fields, api


class Project(models.Model):
    _inherit = "project.task"

    vehicle_id = fields.Many2one(related="project_id.vehicle_id")

    vehicle_count = fields.Integer(string="Vehicle Count", compute='_compute_vehicle_count')

    @api.depends('vehicle_id')
    def _compute_vehicle_count(self):
        for rec in self:
            rec.vehicle_count = 1 if rec.vehicle_id else 0

    def open_view_vehicle(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Vehicle",
            "res_model": "product.template",
            "view_mode": "form",
            "res_id": self.vehicle_id.id,
        }
