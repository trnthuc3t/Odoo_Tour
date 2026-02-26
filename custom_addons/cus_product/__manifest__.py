# -*- coding: utf-8 -*-
{
    'name': 'Custom Product Management',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Quản lý sản phẩm tùy chỉnh cho Odoo 17',
    'description': """
        Module quản lý sản phẩm tùy chỉnh
        ===================================
        * Quản lý thông tin sản phẩm chi tiết
        * Theo dõi giá bán, giá vốn và lợi nhuận
        * Quản lý tồn kho và số lượng đã bán
        * Phân loại sản phẩm theo danh mục
        * Tính toán tự động các chỉ số lợi nhuận
        * Hỗ trợ mã vạch và hình ảnh sản phẩm
    """,
    'author': 'Thuc',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}