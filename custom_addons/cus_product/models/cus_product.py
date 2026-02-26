# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CusProduct(models.Model):
    _name = 'cus.product'
    _description = 'Quản lý sản phẩm tùy chỉnh'
    _order = 'name'
    _rec_name = 'name'

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
        ('furniture', 'Nội thất'),
        ('other', 'Khác'),
    ], string='Danh mục', default='other', required=True)

    price = fields.Float(
        string='Giá bán',
        digits=(10, 2),
        default=0.0,
        help='Giá bán của sản phẩm (VNĐ)'
    )

    cost = fields.Float(
        string='Giá vốn',
        digits=(10, 2),
        default=0.0,
        help='Giá vốn của sản phẩm (VNĐ)'
    )

    quantity = fields.Integer(
        string='Số lượng tồn kho',
        default=0,
        help='Số lượng sản phẩm trong kho'
    )

    quantity_sold = fields.Integer(
        string='Số lượng đã bán',
        default=0,
        readonly=True,
        help='Tổng số lượng sản phẩm đã bán'
    )

    active = fields.Boolean(
        string='Hoạt động',
        default=True,
        help='Bỏ chọn để ẩn sản phẩm mà không xóa'
    )

    image = fields.Binary(
        string='Hình ảnh sản phẩm',
        help='Upload hình ảnh sản phẩm'
    )

    state = fields.Selection([
        ('draft', 'Nháp'),
        ('available', 'Có sẵn'),
        ('out_of_stock', 'Hết hàng'),
        ('discontinued', 'Ngừng kinh doanh'),
    ], string='Trạng thái', default='draft', required=True, tracking=True)

    profit = fields.Float(
        string='Lợi nhuận/sp',
        compute='_compute_profit',
        store=True,
        digits=(10, 2),
        help='Lợi nhuận trên mỗi sản phẩm = Giá bán - Giá vốn'
    )

    total_profit = fields.Float(
        string='Tổng lợi nhuận',
        compute='_compute_total_profit',
        store=True,
        digits=(10, 2),
        help='Tổng lợi nhuận = Lợi nhuận/sp × Số lượng đã bán'
    )

    margin_percent = fields.Float(
        string='% Lợi nhuận',
        compute='_compute_margin_percent',
        store=True,
        digits=(5, 2),
        help='Phần trăm lợi nhuận = (Lợi nhuận/Giá vốn) × 100'
    )

    total_value = fields.Float(
        string='Giá trị tồn kho',
        compute='_compute_total_value',
        store=True,
        digits=(12, 2),
        help='Giá trị tổng = Giá vốn × Số lượng tồn'
    )

    barcode = fields.Char(
        string='Mã vạch',
        copy=False,
        help='Mã vạch sản phẩm'
    )

    weight = fields.Float(
        string='Trọng lượng (kg)',
        digits=(8, 2),
        default=0.0,
        help='Trọng lượng sản phẩm tính bằng kg'
    )

    note = fields.Text(
        string='Ghi chú',
        help='Ghi chú thêm về sản phẩm'
    )

    # Constraints SQL
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Mã sản phẩm phải là duy nhất!'),
        ('barcode_unique', 'UNIQUE(barcode)', 'Mã vạch phải là duy nhất!'),
    ]

    # Computed fields
    @api.depends('price', 'cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.price - record.cost

    @api.depends('profit', 'quantity_sold')
    def _compute_total_profit(self):
        for record in self:
            record.total_profit = record.profit * record.quantity_sold

    @api.depends('profit', 'cost')
    def _compute_margin_percent(self):
        for record in self:
            if record.cost > 0:
                record.margin_percent = (record.profit / record.cost) * 100
            else:
                record.margin_percent = 0.0

    @api.depends('cost', 'quantity')
    def _compute_total_value(self):
        for record in self:
            record.total_value = record.cost * record.quantity

    # Constraints
    @api.constrains('price', 'cost')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError('Giá bán không được nhỏ hơn 0!')
            if record.cost < 0:
                raise ValidationError('Giá vốn không được nhỏ hơn 0!')

    @api.constrains('quantity', 'quantity_sold')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError('Số lượng tồn kho không được âm!')
            if record.quantity_sold < 0:
                raise ValidationError('Số lượng đã bán không được âm!')

    @api.constrains('weight')
    def _check_weight(self):
        for record in self:
            if record.weight < 0:
                raise ValidationError('Trọng lượng không được âm!')

    # Onchange methods
    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.quantity == 0 and self.state == 'available':
            self.state = 'out_of_stock'
        elif self.quantity > 0 and self.state == 'out_of_stock':
            self.state = 'available'

    # Action methods
    def action_set_available(self):
        """Đặt trạng thái sản phẩm thành Có sẵn"""
        self.write({'state': 'available'})

    def action_set_out_of_stock(self):
        """Đặt trạng thái sản phẩm thành Hết hàng"""
        self.write({'state': 'out_of_stock'})

    def action_set_discontinued(self):
        """Ngừng kinh doanh sản phẩm"""
        self.write({'state': 'discontinued', 'active': False})

    def action_restock(self):
        """Nhập thêm hàng vào kho"""
        return {
            'name': 'Nhập hàng',
            'type': 'ir.actions.act_window',
            'res_model': 'cus.product',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def sell_product(self, quantity):
        """
        Bán sản phẩm
        :param quantity: Số lượng bán
        """
        self.ensure_one()
        if quantity <= 0:
            raise ValidationError('Số lượng bán phải lớn hơn 0!')
        if self.quantity < quantity:
            raise ValidationError(f'Không đủ hàng trong kho! Chỉ còn {self.quantity} sản phẩm.')

        self.write({
            'quantity': self.quantity - quantity,
            'quantity_sold': self.quantity_sold + quantity,
        })

    @api.model
    def create(self, vals):
        """Override create để tự động set trạng thái"""
        if vals.get('quantity', 0) > 0 and vals.get('state') == 'draft':
            vals['state'] = 'available'
        return super(CusProduct, self).create(vals)
