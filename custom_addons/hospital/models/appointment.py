from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
import random

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'name'
    _order = 'id desc'


    name = fields.Char(string='Sequence',default='New')
    patient_id = fields.Many2one('hospital.patient',string='Patient',ondelete='restrict') # when using ondelete='cascade' then when patient delete its corresponding appointment deleted.
    appointment_time = fields.Datetime(string='Appointment Time',default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date',default=fields.Date.context_today)
    gender = fields.Selection(related='patient_id.gender')
    ref = fields.Char(string='Reference',help='Reference from  patient record')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft','Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')],string='Status',default='draft',required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines','appointment_id',string='Pharmacy Line')
    hide_sales_price = fields.Boolean(string='Hide sale Price')
    operation_id = fields.Many2one('hospital.operation',string='Operation')
    progress = fields.Integer(string='Progress',compute='_compute_progress')
    duration = fields.Float(string='Duration')
    company_id = fields.Many2one('res.company',string='Company',default=lambda self:self.env.company)
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    total_price = fields.Monetary(string='Total Price', compute='_compute_total_price', currency_field='currency_id')

    @api.depends('pharmacy_line_ids.price_subtotal')
    def _compute_total_price(self):
        for rec in self:
            total = sum(line.price_subtotal for line in rec.pharmacy_line_ids)
            rec.total_price = total
    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0,25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25,75)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def notification_button(self):
        action = self.env.ref('hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Click here to move patient details'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky': True,
                'next':{
                    'type':'ir.actions.act_window',
                    'res_model':'hospital.patient',
                    'res_id':self.patient_id.id,
                    'views':[(False,'form')]
                }
            },
        }

    def object_button(self):

            # url action
           return {
               'type':'ir.actions.act_url',
               'target':'self',
               'url':'https://www.odoo.com/'
           }


        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'button clicked',
        #         'type': 'rainbow_man',
        #     }
        # }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_cancel(self):
        # for rec in self:
        #     rec.state = 'cancel'
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        print("test")
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_('Patient has no whatsapp number.'))
        message = "Hi *%s*, your *appointment* number is : %s,Thank you." % (self.patient_id.name,self.name)
        whatsapp_url = 'https://web.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone,message)

        self.message_post(body=message,subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_url
        }

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://www.levelupreader.com/app/#/login?redirect=%2Fbookshelf%2F',
        }

    def action_send_mail(self):
        template = self.env.ref('hospital.appointment_mail_template')
        for rec in self:
            if rec.patient_id.email:
                template.send_mail(rec.id)



    def serial_number(self):
        s_number = 0
        for num in self.pharmacy_line_ids:
            s_number += 1
            num.s_number = s_number
        return

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        res.serial_number()
        return res

    def unlink(self):
        if self.state != 'draft':
            print(self.state)
            raise ValidationError(_('You cannot delete appointment.'))
        return super(HospitalAppointment, self).unlink()
    def write(self, vals):

        # if not self.ref and not vals.get('ref'):
        #     vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
            res = super(HospitalAppointment, self).write(vals)
            self.serial_number()
            return res

class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product',required=True)
    price_unit = fields.Float(string='Price',related='product_id.list_price',digits='Product Price')
    qty = fields.Integer(string='Quantity',default=1)
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')
    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    price_subtotal = fields.Monetary(string='Subtotal',compute='_compute_subtotal',currency_field='currency_id')
    s_number = fields.Integer(string='SR.NO')


    @api.depends('price_unit','qty')
    def _compute_subtotal(self):

        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty


