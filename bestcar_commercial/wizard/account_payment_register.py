from odoo import models, Command


class AccountPaymentRegister(models.TransientModel):
     _inherit = "account.payment.register"

     def action_create_payments(self):
        res = super().action_create_payments()
        for wizard in self:
            for line in wizard.line_ids.filtered(lambda l:l.move_id.move_type == "out_invoice").move_id.invoice_line_ids:
                        product = line.product_id
                        if product.is_vehicle and not product.trade_in and product.status == 'payment':
                            product.status = "waiting_TI"
                            if product.project_ids:
                                last_project_id = product.product_tmpl_id.project_ids[-1]
                                self.env['project.task'].create([
                                    {'name': f"{product.product_tmpl_id.name} CT", 'project_id': last_project_id.id,
                                     'user_ids': [Command.set([
                                         last_project_id.user_id.id])],
                                     'priority': '1'}])
        return res
