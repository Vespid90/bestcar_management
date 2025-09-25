from odoo import models, fields

PROJECT_STAGES = [
    {'name': 'New', 'sequence': 1},
    {'name': 'In Progress', 'sequence': 2},
    {'name': 'Done', 'sequence': 3},
    {'name': 'Cancelled', 'sequence': 4}
]


class Project(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        department = self.env.ref('bestcar_commercial.hr_department_mechanical_workshop')
        manager_user = department.manager_id.user_id
        default_user_id = manager_user.id if manager_user else self.env.uid

        for order in self:
            for order_line in order.order_line:
                if order_line.product_id.is_vehicle:
                    order_line.product_id.date_purchase = fields.Date.today()
                    order_line.product_id.purchase_price = order_line.price_unit
                    order_line.product_id.supplier_id = order_line.partner_id
                    order_line.product_id.status = "waiting_arrival"
                    project = self.env['project.project'].create({
                        'active': True,
                        'name': f"{order_line.product_id.name} Reconditioning",
                        'user_id': default_user_id,
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
                        {'name': f"{order_line.product_id.name} Inspection", 'project_id': project.id,
                         'user_ids': [(6, 0, [
                             default_user_id])],
                         'priority': '1'},
                        {'name': f"{order_line.product_id.name} Repair", 'project_id': project.id, 'user_ids': [(6, 0, [
                            default_user_id])]},
                        {'name': f"{order_line.product_id.name} Maintenance", 'project_id': project.id,
                         'user_ids': [(6, 0, [
                             default_user_id])]},
                        {'name': f"{order_line.product_id.name} Cleaning", 'project_id': project.id,
                         'user_ids': [(6, 0, [
                             default_user_id])]}
                    ])
        return super().button_confirm()

    def button_cancel(self):
        res = super().button_cancel()
        for order in self:
            for order_line in order:
                if order_line.product_id.is_vehicle:
                    order_line.product_id.status = "added"

        return res
