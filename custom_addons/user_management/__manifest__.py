# -*- coding: utf-8 -*-
{
    'name': 'User Management',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Quản lý người dùng',
    'description': """
        Module quản lý người dùng
        ========================
        * Quản lý thông tin người dùng
        * Tạo tài khoản người dùng
        * Kích hoạt/Archived hàng loạt
        * Lưu trữ ảnh đại diện
    """,
    'author': 'Thuc',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/user_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
