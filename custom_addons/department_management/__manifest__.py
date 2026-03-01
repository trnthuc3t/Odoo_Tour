# -*- coding: utf-8 -*-
{
    'name': 'Department Management',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Quản lý phòng ban',
    'description': """
        Module quản lý phòng ban
        ========================
        * Quản lý thông tin phòng ban
        * Chọn trưởng phòng cho mỗi phòng ban
    """,
    'author': 'Thuc',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/department_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
