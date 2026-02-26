# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request


class HomeDashboard(http.Controller):

    @http.route('/home', type='http', auth='user', website=True)
    def home_dashboard(self, **kw):
        """Hiển thị trang home với danh sách các module khả dụng."""

        # Lấy danh sách các module đã cài đặt và là ứng dụng chính
        modules = request.env['ir.module.module'].sudo().search([
            ('state', '=', 'installed'),
            ('application', '=', True)
        ], order='shortdesc asc')

        # Chuẩn bị dữ liệu cho template
        module_list = []
        search_items = []  # Cho command palette

        # Add Settings "module"
        module_list.append({
            'name': 'Settings',
            'short_name': 'Settings',
            'technical_name': 'base_setup',
            'description': 'Cấu hình hệ thống',
            'icon_paths': ['/base/static/description/settings.png', '/web/static/img/default_icon.png'],
            'url': '/web#action=base.action_res_company_form',
            'is_settings': True,
        })
        search_items.append({
            'type': 'module',
            'name': 'Settings',
            'description': 'Cấu hình hệ thống',
            'keywords': 'settings config configuration thiet lap cau hinh',
            'url': '/web#action=base.action_res_company_form',
        })

        for module in modules:
            # Tạo URL mặc định
            module_url = '/web'

            # Lấy icon - thử các đường dẫn phổ biến
            icon_paths = [
                f'/{module.name}/static/description/icon.png',
                f'/base/static/img/icons/{module.name}.png',
            ]

            # Tạo short name (tối đa 12 ký tự)
            full_name = module.shortdesc or module.name
            short_name = full_name[:12] + '...' if len(full_name) > 12 else full_name

            module_list.append({
                'name': full_name,
                'short_name': short_name,
                'technical_name': module.name,
                'description': module.summary or module.name,
                'icon_paths': icon_paths,
                'url': module_url,
            })

            # Add to search items
            search_items.append({
                'type': 'module',
                'name': full_name,
                'description': module.summary or full_name,
                'keywords': f"{full_name} {module.name} {module.summary or ''}".lower(),
                'url': module_url,
            })

        # Lấy các menu phổ biến cho tìm kiếm
        menus = request.env['ir.ui.menu'].sudo().search([
            ('parent_id', '!=', False),
            ('action', '!=', False),
        ], limit=50)

        for menu in menus:
            if menu.action:
                action_url = f'/web#action={menu.action.id}'
                search_items.append({
                    'type': 'menu',
                    'name': menu.name,
                    'description': menu.parent_id.name if menu.parent_id else '',
                    'keywords': f"{menu.name} {menu.parent_id.name if menu.parent_id else ''}".lower(),
                    'url': action_url,
                })

        # Prepare user data for avatar
        user = request.env.user
        user_name = user.name or ''
        name_parts = user_name.split()
        initials = ''
        if name_parts:
            initials = name_parts[0][0]
            if len(name_parts) > 1:
                initials += name_parts[-1][0]
        initials = initials.upper()

        # Generate avatar color based on user name
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#e91e63']
        color_index = sum(ord(c) for c in user_name) % len(colors)
        avatar_color = colors[color_index]

        return request.render('home_dashboard.home_page', {
            'modules': module_list,
            'search_items': search_items,
            'user': user,
            'user_initials': initials,
            'avatar_color': avatar_color,
        })
