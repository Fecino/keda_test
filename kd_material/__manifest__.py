{
    'name': 'Material Registry',
    'version': '14.0.1.0.0',
    'summary': 'Modul untuk registrasi dan manajemen material yang akan dijual.',
    'description': """
        Modul ini memungkinkan pengguna untuk:
        - Mendaftarkan material (Fabric, Jeans, Cotton)
        - Menentukan harga beli dan supplier
        - Melihat, memfilter, mengubah, dan menghapus material
        - Mengakses data material via REST API
    """,
    'author': 'Achmad Fecino Reinaldi',
    'website': '-',
    'category': 'Inventory',
    'depends': ['base'],
    'data': [
        'security/rule.xml',
        'security/ir.model.access.csv',
        'views/material_views.xml',
    ],
    'installable': True,
    'application': True,
}
