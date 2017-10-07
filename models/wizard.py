# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = "openacademy.wizard"

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_id'))
    session_ids = fields.Many2many('openacademy.session',
        string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attender_ids |= self.attendee_ids
        return {}
