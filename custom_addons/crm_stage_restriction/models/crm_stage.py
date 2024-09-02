from odoo import models, fields, api
from odoo.exceptions import UserError

class CRMStage(models.Model):
    _inherit = 'crm.stage'

    restrict_movement = fields.Boolean(string='Restrict Movement')


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    @api.constrains('stage_id')
    def _check_stage_restriction(self):
        for lead in self:
            if lead.stage_id.restrict_movement:
                if not self.env.user.has_group('crm_stage_restriction.group_restricted_stage_move'):
                    raise UserError('You cannot move to this stage.')
