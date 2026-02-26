# -*- coding: utf-8 -*-
{
    'name': 'Home Dashboard',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Trang home hiển thị danh sách các module khả dụng',
    'description': """
        Home Dashboard
        ================
        * Hiển thị danh sách các module đã cài đặt dưới dạng grid
        * Click vào module để điều hướng đến action/menu tương ứng
        * Tự động chuyển đến /home sau khi đăng nhập
        * Giao diện đẹp, responsive

        Cài đặt xong, truy cập: http://localhost:8069/home
    """,
    'author': 'Thuc',
    'depends': ['base', 'web'],
    'data': [
        'views/home_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
