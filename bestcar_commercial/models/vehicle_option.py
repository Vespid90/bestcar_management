from odoo import models, fields

class VehicleOption(models.Model):
    _name = 'vehicle.option'
    _description = 'Vehicle Option'
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)

    product_tmpl_ids = fields.Many2many(
        'product.template',
        'product_template_vehicle_option_rel',
        'option_id', 'product_tmpl_id',
        string='Vehicles',
        domain=[('is_vehicle', '=', True)],
    )

