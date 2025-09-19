from odoo import models

class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def action_create_payments(self):
        res = super().action_create_payments()
        for wizard in self:
            for line in wizard.line_ids:
                move = line.move_id
                print("test1")
                if move.move_type == "out_invoice":
                    for invoice_line in move.invoice_line_ids:
                        product = invoice_line.product_id
                        if product.product_tmpl_id.is_vehicle:
                            print("test2")
                            product.product_tmpl_id.status = "waiting_delivery"
        return res