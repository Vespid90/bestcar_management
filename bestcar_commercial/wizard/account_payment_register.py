from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        res = super().action_create_payments()
        for wizard in self:
            for line in wizard.line_ids:
                move = line.move_id
                if move.move_type == "out_invoice":
                    for invoice_line in move.invoice_line_ids:
                        product = invoice_line.product_id
                        if product.product_tmpl_id.is_vehicle and not product.product_tmpl_id.trade_in:
                            product.product_tmpl_id.status = "waiting_TI"
                            last_project_id = product.product_tmpl_id.project_ids[-1]
                            self.env['project.task'].create([
                                {'name': f"{product.product_tmpl_id.name} CT", 'project_id': last_project_id.id,
                                 'user_ids': [(6, 0, [
                                     last_project_id.user_id.id])],
                                 'priority': '1'}])
        return res
