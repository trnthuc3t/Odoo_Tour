# -*- coding: utf-8 -*-
from odoo import models, fields


class Department(models.Model):
    _name = 'custom.department'
    _description = 'Phòng ban'
    _order = 'name'

    name = fields.Char(string='Tên phòng ban', required=True)
    manager_id = fields.Many2one(
        'res.users',
        string='Trưởng phòng',
        ondelete='set null',
    )
