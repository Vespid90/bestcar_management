from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        res = super()._action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_template_id.is_vehicle:
                    line.product_template_id.status = "reserved"
        return res

    def action_cancel(self):
        res = super().action_cancel()
        for order in self:
            for line in order.order_line:
                if line.product_template_id.is_vehicle:
                    line.product_template_id.status = "for_sale"
        return res
