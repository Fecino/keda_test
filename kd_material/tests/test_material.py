from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestMaterialModel(TransactionCase):

    def setUp(self):
        super(TestMaterialModel, self).setUp()
        self.Material = self.env['kd_material.material']
        self.Currency = self.env.ref('base.USD')
        self.Partner = self.env['res.partner'].create({
            'name': 'Test Supplier'
        })

    def test_create_valid_material(self):
        material = self.Material.create({
            'name': 'Test Material',
            'code': 'TM01',
            'type': 'fabric',
            'buy_price': 200.0,
            'currency_id': self.Currency.id,
            'supplier_id': self.Partner.id
        })
        self.assertTrue(material.id)
        self.assertEqual(material.code, 'TM01')

    def test_duplicate_code(self):
        self.Material.create({
            'name': 'Material 1',
            'code': 'DUP01',
            'type': 'cotton',
            'buy_price': 300.0,
            'currency_id': self.Currency.id,
            'supplier_id': self.Partner.id
        })

        with self.assertRaises(IntegrityError):
            self.Material.create({
                'name': 'Material 2',
                'code': 'DUP01',
                'type': 'jeans',
                'buy_price': 350.0,
                'currency_id': self.Currency.id,
                'supplier_id': self.Partner.id
            })

    def test_buy_price_check_constraint(self):
        with self.assertRaises(IntegrityError):
            self.Material.create({
                'name': 'Cheap Material',
                'code': 'CHEAP',
                'type': 'cotton',
                'buy_price': 50.0,  # Below threshold
                'currency_id': self.Currency.id,
                'supplier_id': self.Partner.id
            })

    def test_name_get_format(self):
        material = self.Material.create({
            'name': 'Formatted Material',
            'code': 'FMT01',
            'type': 'jeans',
            'buy_price': 400.0,
            'currency_id': self.Currency.id,
            'supplier_id': self.Partner.id
        })
        display_name = material.name_get()[0][1]
        self.assertEqual(display_name, '[FMT01] Formatted Material')

    def test_name_search(self):
        material = self.Material.create({
            'name': 'Searchable Material',
            'code': 'SRC01',
            'type': 'fabric',
            'buy_price': 250.0,
            'currency_id': self.Currency.id,
            'supplier_id': self.Partner.id
        })

        results = self.Material._name_search('SRC01')
        self.assertTrue(material.id in results)
