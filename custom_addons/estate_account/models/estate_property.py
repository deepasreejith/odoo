from odoo import models, api
from odoo import Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        for property in self:
            if property.buyer_id:
                # Calculate invoice line amounts
                selling_price = property.selling_price
                tax_amount = selling_price * 0.06
                administrative_fees = selling_price + 100.00

                # Create invoice values
                invoice_vals = {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        # Invoice line for tax (6% of the selling price)
                        Command.create({

                            'name': 'Tax (6%)',
                            'quantity': len(property.offer_ids),
                            'price_unit': tax_amount,
                        }),
                        # Invoice line for administrative fees ($100.00)
                        Command.create({
                           
                            'name': 'Administrative Fees',
                            'quantity': len(property.offer_ids),
                            'price_unit': administrative_fees,
                        })
                    ]
                }

                # Create account move with invoice and invoice lines
                account_move = self.env['account.move'].create(invoice_vals)

            else:
                print("No buyer assigned for property")