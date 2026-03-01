# -*- coding: utf-8 -*-
{
    'name': 'Home Dashboard',
    'version': '17.0.1.0.0',
    'category': 'Thuc Custom Modules',
    'summary': 'Giao diện home menu dạng full-screen overlay',
    'author': 'Thuc',
    'depends': ['base', 'web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'home_dashboard/static/src/css/apps_menu.scss',
            'home_dashboard/static/src/js/apps_menu.js',
            'home_dashboard/static/src/xml/apps_menu.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
