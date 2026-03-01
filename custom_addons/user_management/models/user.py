# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UserProfile(models.Model):
    _name = 'user.profile'
    _description = 'Quản lý người dùng'
    _order = 'name'

    name = fields.Char(string='Họ và tên', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Số điện thoại')
    image = fields.Image(string='Ảnh đại diện', max_width=256, max_height=256)
    active = fields.Boolean(string='Hoạt động', default=True)
    password = fields.Char(string='Mật khẩu', store=False, copy=False)
    user_id = fields.Many2one('res.users', string='User Odoo', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        # Tạo user profile trước
        profile = super().create(vals)

        # Nếu có email và password, tạo user trong res.users
        if vals.get('email') and vals.get('password'):
            self._create_or_update_user(profile, vals.get('password'))

        return profile

    def write(self, vals):
        # Lưu password trước khi xóa khỏi vals
        password = vals.get('password')

        # Nếu password rỗng thì không cập nhật
        if password == '':
            vals.pop('password', None)

        result = super().write(vals)

        # Cập nhật user trong res.users nếu có password mới
        if password:
            for profile in self:
                if profile.user_id and password:
                    profile.user_id.sudo().write({'password': password})
                elif not profile.user_id and profile.email and password:
                    self._create_or_update_user(profile, password)

        # Cập nhật thông tin user nếu thay đổi
        if 'name' in vals or 'email' in vals or 'image' in vals:
            for profile in self:
                if profile.user_id:
                    user_vals = {}
                    if 'name' in vals:
                        user_vals['name'] = vals['name']
                    if 'email' in vals:
                        user_vals['login'] = vals['email']
                    if 'image' in vals:
                        user_vals['image_1920'] = vals.get('image')
                    if user_vals:
                        profile.user_id.sudo().write(user_vals)

        return result

    def _create_or_update_user(self, profile, password):
        """Tạo hoặc cập nhật user trong res.users"""
        if not profile.email:
            return

        # Kiểm tra user đã tồn tại chưa (dùng sudo vì cần quyền)
        existing_user = self.env['res.users'].sudo().search([('login', '=', profile.email)])

        user_vals = {
            'name': profile.name,
            'login': profile.email,
            'password': password,
            'image_1920': profile.image if profile.image else False,
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        }

        if existing_user:
            existing_user.sudo().write(user_vals)
            profile.user_id = existing_user.id
        else:
            new_user = self.env['res.users'].sudo().create(user_vals)
            profile.user_id = new_user.id

    def action_activate(self):
        self.write({'active': True})
        for profile in self:
            if profile.user_id:
                profile.user_id.sudo().write({'active': True})

    def action_archive(self):
        self.write({'active': False})
        for profile in self:
            if profile.user_id:
                profile.user_id.sudo().write({'active': False})
