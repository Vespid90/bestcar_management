from odoo import models, fields


class BestcarCommercial(models.Model):
    _name = 'bestcar.commercial'
    _description = 'bestcar commercial'

    name = fields.Char(string="Car")
