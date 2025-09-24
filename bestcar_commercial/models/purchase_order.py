from odoo import models, fields, api

PROJECT_STAGES = [
    {'name': 'New', 'sequence': 1},
    {'name': 'In Progress', 'sequence': 2},
    {'name': 'Done', 'sequence': 3},
    {'name': 'Cancelled', 'sequence': 4}
    ]

class Project(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super().button_confirm()

        for order in self:
            for order_line in order:
                if order_line.product_id.is_vehicle:
                    order_line.product_id.status = "waiting_arrival"

                    department = self.env['hr.department'].search([('id', '=',8)],limit=1)
                    project = self.env['project.project'].create({
                                'active': True,
                                'name': f"{order_line.product_id.name} Reconditioning",
                                'user_id': department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id,
                                'vehicle_id': order_line.product_id.product_tmpl_id.id,
                            })
                    stages_to_create = []
                    for stage in PROJECT_STAGES:
                        stages_to_create.append({
                            'name': stage['name'],
                            'sequence': stage['sequence'],
                            'project_ids': [(4, project.id)],
                        })
                    self.env['project.task.type'].create(stages_to_create)
                    self.env['project.task'].create([
                            {'name': f"{order_line.product_id.name} Inspection", 'project_id': project.id, 'user_ids': [(6, 0, [
                                department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])],
                                'priority': '1'},
                            {'name': f"{order_line.product_id.name} Repair", 'project_id': project.id, 'user_ids': [(6, 0, [
                                department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])]},
                            {'name': f"{order_line.product_id.name} Maintenance", 'project_id': project.id, 'user_ids': [(6, 0, [
                                department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])]},
                            {'name': f"{order_line.product_id.name} Cleaning", 'project_id': project.id, 'user_ids': [(6, 0, [
                                department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])]}
                            ])
        return res
