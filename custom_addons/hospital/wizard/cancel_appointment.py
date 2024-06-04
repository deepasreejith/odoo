from odoo import fields, models, api, _
import datetime
from datetime import date
from odoo.exceptions import ValidationError
from  dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    @api.model
    def default_get(self, fields):
        print("default get executed", fields)
        res = super(CancelAppointmentWizard, self).default_get(fields)
        print(res)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
           res['appointment_id'] = self.env.context.get('active_id')

        return res

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment',domain=[('state','=','draft'),('priority','in',('0','1',False))])
    reason = fields.Text(string='Reason')
    date_cancel = fields.Date(string='Cancellation Date')

    def cancel_appointment(self):
        cancel_day = self.env['ir.config_parameter'].get_param('hospital.cancel_days')
        allow_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        print(cancel_day)
        print(allow_date)
        if allow_date < date.today():
            raise ValidationError(_("cancellation not allowed this date of booking"))
        # if self.appointment_id.booking_date == fields.Date.today():
        #     raise ValidationError(_("cancellation not allowed same date of booking"))
        self.appointment_id.state = 'cancel'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
