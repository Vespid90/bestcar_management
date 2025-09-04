from odoo import models, fields, api


class product_template(models.Model):
    _inherit = "product.template"

    active = fields.Boolean(default=True)
    name = fields.Char('Name', required=True)
    image = fields.Image("Logo", max_width=128, max_height=128)

