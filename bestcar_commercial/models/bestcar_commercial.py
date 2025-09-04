from odoo import models, fields, api


class bestcar_commercial(models.Model):
    _name = 'bestcar.commercial'
    _description = 'bestcar commercial'

    name = fields.Char(string="voiture")