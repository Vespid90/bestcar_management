from odoo import models, fields


class Project(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        for rec in self:
            if rec.product_id.product_tmpl_id.is_vehicle:
                if rec.product_id.product_tmpl_id.status == "waiting_arrival":
                    rec.product_id.product_tmpl_id.date_arrival = fields.Date.today()
                    rec.product_id.product_tmpl_id.status = "reconditioning"
                else:
                    rec.product_id.product_tmpl_id.status = "delivered"
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for rec in self:
            if rec.product_id.product_tmpl_id.is_vehicle:
                if rec.product_id.product_tmpl_id.status == "waiting_arrival":
                    rec.product_id.product_tmpl_id.status = "added"
                else:
                    rec.product_id.product_tmpl_id.status = "for_sale"
        return res
