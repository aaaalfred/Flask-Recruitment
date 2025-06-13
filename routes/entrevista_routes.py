from flask import Blueprint, request, jsonify
from services.auth_service import token_required
from models import Entrevista, Candidato, Vacante, db
from datetime import datetime

entrevista_bp = Blueprint('entrevista', __name__)

@entrevista_bp.route('', methods=['GET'])
@token_required
def get_entrevistas(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        
        query = Entrevista.query
        
        # Filtrar por fechas si se proporcionan
        if fecha_desde:
            query = query.filter(Entrevista.fecha >= datetime.fromisoformat(fecha_desde))
        if fecha_hasta:
            query = query.filter(Entrevista.fecha <= datetime.fromisoformat(fecha_hasta))
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            # Solo entrevistas de candidatos asignados al reclutador
            query = query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        
        entrevistas = query.order_by(Entrevista.fecha.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'entrevistas': [entrevista.to_dict() for entrevista in entrevistas.items],
            'total': entrevistas.total,
            'pages': entrevistas.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo entrevistas: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['GET'])
@token_required
def get_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver esta entrevista'}), 403
        
        return jsonify(entrevista.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo entrevista: {str(e)}'}), 500

@entrevista_bp.route('', methods=['POST'])
@token_required
def create_entrevista(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['fecha', 'tipo', 'candidato_id', 'vacante_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar que candidato y vacante existen
        candidato = Candidato.query.get(data['candidato_id'])
        vacante = Vacante.query.get(data['vacante_id'])
        
        if not candidato:
            return jsonify({'message': 'Candidato no encontrado'}), 404
        if not vacante:
            return jsonify({'message': 'Vacante no encontrada'}), 404
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para programar entrevista a este candidato'}), 403
        
        nueva_entrevista = Entrevista(
            fecha=datetime.fromisoformat(data['fecha']),
            tipo=data['tipo'],
            candidato_id=data['candidato_id'],
            vacante_id=data['vacante_id'],
            entrevistador_id=current_user.id,
            comentarios=data.get('comentarios'),
            duracion_minutos=data.get('duracion_minutos'),
            ubicacion=data.get('ubicacion')
        )
        
        db.session.add(nueva_entrevista)
        db.session.commit()
        
        return jsonify({
            'message': 'Entrevista creada exitosamente',
            'entrevista': nueva_entrevista.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'message': 'Formato de fecha inválido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando entrevista: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['PUT'])
@token_required
def update_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar esta entrevista'}), 403
        
        data = request.get_json()
        
        # Campos actualizables
        if 'fecha' in data:
            entrevista.fecha = datetime.fromisoformat(data['fecha'])
        if 'tipo' in data:
            entrevista.tipo = data['tipo']
        if 'resultado' in data:
            entrevista.resultado = data['resultado']
        if 'comentarios' in data:
            entrevista.comentarios = data['comentarios']
        if 'puntuacion' in data:
            entrevista.puntuacion = data['puntuacion']
        if 'duracion_minutos' in data:
            entrevista.duracion_minutos = data['duracion_minutos']
        if 'ubicacion' in data:
            entrevista.ubicacion = data['ubicacion']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Entrevista actualizada exitosamente',
            'entrevista': entrevista.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'message': 'Formato de fecha inválido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando entrevista: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['DELETE'])
@token_required
def delete_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para eliminar esta entrevista'}), 403
        
        db.session.delete(entrevista)
        db.session.commit()
        
        return jsonify({'message': 'Entrevista eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando entrevista: {str(e)}'}), 500
