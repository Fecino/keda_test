"""
Material model representing material registrations in the Odoo system.

This model manages material information including unique identification, 
classification, pricing, and supplier details. It provides constraints 
to ensure data integrity such as unique material codes and minimum pricing.

Key Features:
- Tracks material name, code, type, and purchase buy_price
- Enforces unique material codes
- Requires material buy_prices to be above 100
- Supports custom name display and search functionality

Fields:
- name: Material name (required)
- code: Unique material code (required)
- type: Material type selection (fabric, jeans, cotton)
- buy_price: Material purchase buy_price
- supplier_id: Associated supplier

Custom methods:
- _check_data: Validates material code uniqueness and buy_price
- name_get: Generates display name with code and name
- _name_search: Enables searching by name or code
"""
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = 'kd_material.material'
    _description = 'Registrasi Material'
    _sql_constraints = [
        ('unique_material_code', 'UNIQUE(code)', 'Material code must be unique!'),
        ('check_material_buy_price', 'CHECK(buy_price > 100)', 'Material buy_price must be above 100!')
    ]

    name = fields.Char(string="Material Name", required=True)
    code = fields.Char(string="Material Code", required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string="Material Type", required=True)
    buy_price = fields.Monetary(string="Material Buy Price", required=True)
    currency_id = fields.Many2one("res.currency", string="Currency", required=True, default=lambda self: self.env.company.currency_id)
    
    # add supplier_rank to domain if needed and if module accunt is installed
    supplier_id = fields.Many2one("res.partner", string="Supplier Name", required=True)

    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            name = f'[{record.code}] {record.name}'
            result.append((record.id, name))
        return result
    
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        return self._search(domain + args, limit=limit)
