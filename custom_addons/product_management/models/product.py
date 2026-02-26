# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = 'product.management'
    _description = 'Quản lý sản phẩm'
    _order = 'name'

    name = fields.Char(
        string='Tên sản phẩm',
        required=True,
        help='Nhập tên sản phẩm'
    )

    code = fields.Char(
        string='Mã sản phẩm',
        required=True,
        copy=False,
        help='Mã định danh duy nhất của sản phẩm'
    )

    description = fields.Text(
        string='Mô tả',
        help='Mô tả chi tiết về sản phẩm'
    )

    category = fields.Selection([
        ('electronics', 'Điện tử'),
        ('clothing', 'Quần áo'),
        ('food', 'Thực phẩm'),
        ('books', 'Sách'),
        ('other', 'Khác'),
    ], string='Danh mục', default='other', required=True)

    price = fields.Float(
        string='Giá bán',
        digits=(10, 2),
        default=0.0,
        help='Giá bán của sản phẩm'
    )

    cost = fields.Float(
        string='Giá vốn',
        digits=(10, 2),
        default=0.0,
        help='Giá vốn của sản phẩm'
    )

    quantity = fields.Integer(
        string='Số lượng',
        default=0,
        help='Số lượng tồn kho'
    )

    active = fields.Boolean(
        string='Hoạt động',
        default=True,
        help='Bỏ chọn để ẩn sản phẩm mà không xóa'
    )

    image = fields.Binary(
        string='Hình ảnh',
        help='Hình ảnh sản phẩm'
    )

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('available', 'Có sẵn'),
        ('out_of_stock', 'Hết hàng'),
    ], string='Trạng thái', default='draft', required=True)

    profit = fields.Float(
        string='Lợi nhuận',
        compute='_compute_profit',
        store=True,
        digits=(10, 2),
        help='Lợi nhuận = Giá bán - Giá vốn'
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Mã sản phẩm phải là duy nhất!'),
    ]

    @api.depends('price', 'cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.price - record.cost

    @api.constrains('price', 'cost')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError('Giá bán không được âm!')
            if record.cost < 0:
                raise ValidationError('Giá vốn không được âm!')

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError('Số lượng không được âm!')

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity == 0:
            self.state = 'out_of_stock'
        elif self.state == 'out_of_stock' and self.quantity > 0:
            self.state = 'available'

    def action_set_available(self):
        self.write({'state': 'available'})

    def action_set_out_of_stock(self):
        self.write({'state': 'out_of_stock'})
