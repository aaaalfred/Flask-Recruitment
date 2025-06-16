from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Cliente, db
from datetime import datetime

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('', methods=['GET'])
@role_required('ejecutivo', 'administrador')
def get_clientes(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search')
        
        query = Cliente.query.filter_by(activo=True)
        
        # Filtrar por búsqueda si se proporciona
        if search:
            query = query.filter(
                db.or_(
                    Cliente.nombre.contains(search),
                    Cliente.ccp.contains(search)
                )
            )
        
        clientes = query.order_by(Cliente.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'clientes': [cliente.to_dict() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo clientes: {str(e)}'}), 500

@cliente_bp.route('/active', methods=['GET'])
@token_required
def get_clientes_activos(current_user):
    """Obtener lista simple de clientes activos para selectors"""
    try:
        clientes = Cliente.query.filter_by(activo=True).order_by(Cliente.nombre).all()
        
        return jsonify({
            'clientes': [
                {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'ccp': cliente.ccp
                } for cliente in clientes
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo clientes activos: {str(e)}'}), 500

@cliente_bp.route('/search', methods=['GET'])
@token_required
def search_clientes(current_user):
    """Búsqueda de clientes para autocomplete"""
    try:
        q = request.args.get('q', '').strip()
        
        if not q:
            return jsonify({'clientes': []}), 200
        
        clientes = Cliente.query.filter(
            Cliente.activo == True,
            db.or_(
                Cliente.nombre.contains(q),
                Cliente.ccp.contains(q)
            )
        ).limit(10).all()
        
        return jsonify({
            'clientes': [
                {
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'ccp': cliente.ccp,
                    'display': f"{cliente.nombre} ({cliente.ccp})"
                } for cliente in clientes
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error en búsqueda de clientes: {str(e)}'}), 500

@cliente_bp.route('/<int:cliente_id>', methods=['GET'])
@role_required('ejecutivo', 'administrador')
def get_cliente(current_user, cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Incluir información adicional
        cliente_dict = cliente.to_dict()
        
        # Agregar estadísticas de vacantes
        cliente_dict['vacantes_detalle'] = [
            {
                'id': vacante.id,
                'nombre': vacante.nombre,
                'estado': vacante.estado,
                'fecha_creacion': vacante.fecha_creacion.isoformat() if vacante.fecha_creacion else None,
                'ejecutivo': vacante.ejecutivo.nombre if vacante.ejecutivo else None,
                'total_candidatos': len(vacante.candidatos_posiciones)
            } for vacante in cliente.vacantes
        ]
        
        return jsonify(cliente_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo cliente: {str(e)}'}), 500

@cliente_bp.route('', methods=['POST'])
@role_required('ejecutivo', 'administrador')
def create_cliente(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'ccp']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Convertir CCP a mayúsculas y limpiar espacios
        ccp = data['ccp'].strip().upper()
        
        # Verificar que el CCP no existe
        existing_cliente = Cliente.query.filter_by(ccp=ccp).first()
        if existing_cliente:
            return jsonify({'message': f'Ya existe un cliente con CCP: {ccp}'}), 400
        
        nuevo_cliente = Cliente(
            nombre=data['nombre'].strip(),
            ccp=ccp
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente creado exitosamente',
            'cliente': nuevo_cliente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando cliente: {str(e)}'}), 500

@cliente_bp.route('/<int:cliente_id>', methods=['PUT'])
@role_required('ejecutivo', 'administrador')
def update_cliente(current_user, cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'nombre' in data:
            cliente.nombre = data['nombre'].strip()
        
        if 'ccp' in data:
            # Convertir CCP a mayúsculas y limpiar
            new_ccp = data['ccp'].strip().upper()
            
            # Verificar que el nuevo CCP no existe (excepto el actual)
            existing = Cliente.query.filter(
                Cliente.ccp == new_ccp,
                Cliente.id != cliente_id
            ).first()
            
            if existing:
                return jsonify({'message': f'Ya existe un cliente con CCP: {new_ccp}'}), 400
            
            cliente.ccp = new_ccp
        
        if 'activo' in data:
            cliente.activo = data['activo']
        
        cliente.fecha_actualizacion = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente actualizado exitosamente',
            'cliente': cliente.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando cliente: {str(e)}'}), 500

@cliente_bp.route('/<int:cliente_id>', methods=['DELETE'])
@role_required('administrador')
def delete_cliente(current_user, cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Verificar si tiene vacantes asociadas
        if cliente.vacantes:
            return jsonify({
                'message': f'No se puede eliminar: el cliente tiene {len(cliente.vacantes)} vacantes asociadas'
            }), 400
        
        # Soft delete - marcar como inactivo
        cliente.activo = False
        cliente.fecha_actualizacion = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Cliente desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando cliente: {str(e)}'}), 500

@cliente_bp.route('/validate-ccp', methods=['POST'])
@role_required('ejecutivo', 'administrador')
def validate_ccp(current_user):
    """Validar si un CCP está disponible"""
    try:
        data = request.get_json()
        ccp = data.get('ccp', '').strip().upper()
        exclude_id = data.get('exclude_id')
        
        if not ccp:
            return jsonify({'valid': False, 'message': 'CCP es requerido'}), 400
        
        query = Cliente.query.filter_by(ccp=ccp)
        
        # Excluir el cliente actual si se está editando
        if exclude_id:
            query = query.filter(Cliente.id != exclude_id)
        
        existing = query.first()
        
        if existing:
            return jsonify({
                'valid': False,
                'message': f'CCP "{ccp}" ya está en uso por: {existing.nombre}'
            }), 200
        
        return jsonify({
            'valid': True,
            'message': f'CCP "{ccp}" está disponible'
        }), 200
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'Error validando CCP: {str(e)}'
        }), 500

# Endpoint adicional para estadísticas de clientes
@cliente_bp.route('/estadisticas', methods=['GET'])
@role_required('ejecutivo', 'administrador')
def get_estadisticas_clientes(current_user):
    """Obtener estadísticas generales de clientes"""
    try:
        total_clientes = Cliente.query.filter_by(activo=True).count()
        clientes_inactivos = Cliente.query.filter_by(activo=False).count()
        
        # Clientes con más vacantes
        clientes_con_vacantes = []
        clientes = Cliente.query.filter_by(activo=True).all()
        
        for cliente in clientes:
            vacantes_count = len(cliente.vacantes)
            if vacantes_count > 0:
                clientes_con_vacantes.append({
                    'id': cliente.id,
                    'nombre': cliente.nombre,
                    'ccp': cliente.ccp,
                    'total_vacantes': vacantes_count,
                    'vacantes_abiertas': len([v for v in cliente.vacantes if v.estado == 'abierta']),
                    'vacantes_cerradas': len([v for v in cliente.vacantes if v.estado == 'cerrada'])
                })
        
        # Ordenar por total de vacantes
        clientes_con_vacantes.sort(key=lambda x: x['total_vacantes'], reverse=True)
        
        estadisticas = {
            'total_clientes': total_clientes,
            'clientes_inactivos': clientes_inactivos,
            'clientes_con_vacantes': clientes_con_vacantes[:10],  # Top 10
            'clientes_sin_vacantes': total_clientes - len(clientes_con_vacantes),
            'fecha_actualizacion': datetime.utcnow().isoformat()
        }
        
        return jsonify(estadisticas), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo estadísticas: {str(e)}'}), 500
