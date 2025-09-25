from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        for move in self:
            for line in move.invoice_line_ids:
                if line.product_id.product_tmpl_id.is_vehicle:
                    line.product_id.product_tmpl_id.status = "payment"
        return res

    def button_cancel(self):
        res = super().button_cancel()
        for move in self:
            for line in move.invoice_line_ids:
                if line.product_id.product_tmpl_id.is_vehicle:
                    line.product_id.product_tmpl_id.status = "for_sale"
        return res
