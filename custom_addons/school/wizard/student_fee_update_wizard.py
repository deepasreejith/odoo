from odoo import fields,models,api


class StudentFeeUpdateWizard(models.TransientModel):
    _name = 'student.fee.update.wizard'

    total_fee = fields.Float(string='Fees')

    def update_fee(self):
        print("click update buttton")
        self.env['student.profile'].browse(self._context.get('active_ids')).update({'total_fee':self.total_fee})
        return True