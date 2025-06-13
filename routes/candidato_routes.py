from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Candidato, db

candidato_bp = Blueprint('candidato', __name__)

@candidato_bp.route('', methods=['GET'])
@token_required
def get_candidatos(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        estado = request.args.get('estado')
        search = request.args.get('search')
        
        query = Candidato.query
        
        # Filtrar por estado
        if estado:
            query = query.filter_by(estado=estado)
        
        # Búsqueda por nombre o email
        if search:
            query = query.filter(
                (Candidato.nombre.contains(search)) |
                (Candidato.email.contains(search))
            )
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.filter_by(reclutador_id=current_user.id)
        
        candidatos = query.order_by(Candidato.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'candidatos': [candidato.to_dict() for candidato in candidatos.items],
            'total': candidatos.total,
            'pages': candidatos.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo candidatos: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['GET'])
@token_required
def get_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver este candidato'}), 403
        
        # Incluir información adicional
        candidato_dict = candidato.to_dict()
        candidato_dict['documentos'] = [doc.to_dict() for doc in candidato.documentos]
        candidato_dict['entrevistas'] = [entrevista.to_dict() for entrevista in candidato.entrevistas]
        candidato_dict['posiciones'] = []
        
        for pos in candidato.candidatos_posiciones:
            candidato_dict['posiciones'].append({
                'id': pos.id,
                'vacante_id': pos.vacante_id,
                'vacante_nombre': pos.vacante.nombre,
                'status': pos.status,
                'nota': pos.nota,
                'fecha_asignacion': pos.fecha_asignacion.isoformat() if pos.fecha_asignacion else None
            })
        
        return jsonify(candidato_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo candidato: {str(e)}'}), 500

@candidato_bp.route('', methods=['POST'])
@role_required('reclutador', 'reclutador_lider')
def create_candidato(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar email único
        if Candidato.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'El email ya existe'}), 400
        
        nuevo_candidato = Candidato(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono'),
            reclutador_id=current_user.id,
            salario_esperado=data.get('salario_esperado'),
            experiencia_anos=data.get('experiencia_anos'),
            ubicacion=data.get('ubicacion'),
            disponibilidad=data.get('disponibilidad'),
            nivel_ingles=data.get('nivel_ingles'),
            linkedin_url=data.get('linkedin_url'),
            comentarios_finales=data.get('comentarios_finales')
        )
        
        db.session.add(nuevo_candidato)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato creado exitosamente',
            'candidato': nuevo_candidato.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando candidato: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['PUT'])
@token_required
def update_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar este candidato'}), 403
        
        data = request.get_json()
        
        # Campos actualizables
        campos_actualizables = [
            'nombre', 'email', 'telefono', 'estado', 'comentarios_finales',
            'salario_esperado', 'experiencia_anos', 'ubicacion', 'disponibilidad',
            'nivel_ingles', 'linkedin_url'
        ]
        
        for campo in campos_actualizables:
            if campo in data:
                # Verificar email único si se está actualizando
                if campo == 'email':
                    existing = Candidato.query.filter_by(email=data[campo]).first()
                    if existing and existing.id != candidato_id:
                        return jsonify({'message': 'El email ya está en uso'}), 400
                
                setattr(candidato, campo, data[campo])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato actualizado exitosamente',
            'candidato': candidato.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando candidato: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['DELETE'])
@role_required('reclutador_lider')
def delete_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Cambiar estado a inactivo en lugar de eliminar
        candidato.estado = 'inactivo'
        db.session.commit()
        
        return jsonify({'message': 'Candidato desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando candidato: {str(e)}'}), 500
