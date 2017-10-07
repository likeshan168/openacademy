# -*- coding: utf-8 -*-

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = "res.partner"
    instructor = fields.Boolean(string="Instructor", default=False)

    session_ids = fields.Many2many("openacademy.session", string="Attedened Sessions", readonly = True)
