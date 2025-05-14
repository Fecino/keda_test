from odoo import http
from odoo.http import request
import json

class MaterialController(http.Controller):
    _MATERIAL_FIELDS = ['code', 'name', 'type', 'price', 'supplier_id']

    def _get_material(self, material_id):
        material = request.env['kd_material.material'].sudo().browse(material_id)
        if not material.exists():
            return {'error': 'Material not found'}, None
        return None, material

    @http.route('/api/materials', auth='user', type='json', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        missing = [field for field in self._MATERIAL_FIELDS if field not in kwargs]
        if missing:
            return {'error': f'Missing fields: {", ".join(missing)}'}
        try:
            material = request.env['kd_material.material'].sudo().create(
                {field: kwargs[field] for field in self._MATERIAL_FIELDS}
            )
        except Exception as e:
            return {'error': f'Failed to create material: {str(e)}'}
        return {'success': True, 'id': material.id}

    @http.route('/api/materials', auth='user', type='http', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        domain = []
        type = kwargs.get('type')
        if type :
            domain.append(('type', '=', type))

        materials = request.env['kd_material.material'].sudo().search_read(
            domain, self._MATERIAL_FIELDS
        )
        return request.make_response(
            json.dumps(materials), 
            headers=[('Content-Type', 'application/json')]
        )

    @http.route('/api/materials/<int:material_id>', auth='user', type='json', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        error, material = self._get_material(material_id)
        if error:
            return error
        try:
            material.sudo().write(kwargs)
        except Exception as e:
            return {'error': f'Failed to update material: {str(e)}'}
        return {'success': True}

    @http.route('/api/materials/<int:material_id>', auth='user', type='json', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        error, material = self._get_material(material_id)
        if error:
            return error

        material.unlink()
        return {'success': True}
