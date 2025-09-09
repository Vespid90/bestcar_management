from odoo import models, fields, api

PROJECT_STAGES = [
    {'name': 'New', 'sequence': 1},
    {'name': 'In Progress', 'sequence': 2},
    {'name': 'Done', 'sequence': 3},
    {'name': 'Cancelled', 'sequence': 4}
    ]

class ProductTemplate(models.Model):
    _inherit = 'product.template'



    @api.model_create_multi
    def create(self,vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        if templates:
            product = templates[0]
            project = self.env['project.project'].create({
                        'active': True,
                        'name': f"{product.name} Reconditioning",
                        'allow_task_dependencies': True
            })
            stages_to_create = []
            for stage in PROJECT_STAGES:
                stages_to_create.append({
                    'name': stage['name'],
                    'sequence': stage['sequence'],
                    'project_ids': [(4, project.id)],  # link stage to project
                })
            self.env['project.task.type'].create(stages_to_create)

            inspection_task = self.env['project.task'].create({
                'name': f"{product.name} Inspection",
                'project_id': project.id,
                'priority': '1'
            })
            print(inspection_task.id)

            self.env['project.task'].create([
                {'name': f"{product.name} Repair",'project_id': project.id, 'depend_on_ids': [(4, inspection_task.id)]},
                {'name': f"{product.name} Maintenance",'project_id': project.id, 'depend_on_ids':[(4, inspection_task.id)]},
                {'name': f"{product.name} Cleaning",'project_id': project.id, 'depend_on_ids': [(4, inspection_task.id)]}
              ])


        return templates
