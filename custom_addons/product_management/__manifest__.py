# -*- coding: utf-8 -*-
{
    'name': 'Product Management',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Quản lý sản phẩm đơn giản',
    'description': """
        Module quản lý sản phẩm
        ========================
        * Quản lý thông tin sản phẩm
        * Theo dõi giá và số lượng
        * Phân loại sản phẩm
    """,
    'author': 'Thuc',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
