from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Usuario, db
from datetime import datetime

vacante_bp = Blueprint('vacante', __name__)

@vacante_bp.route('', methods=['GET'])
@token_required
def get_vacantes(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        estado = request.args.get('estado')
        avance = request.args.get('avance')
        search = request.args.get('search')  # ⭐ NUEVO - Búsqueda por nombre
        cliente = request.args.get('cliente')  # ⭐ NUEVO - Búsqueda por cliente/CCP
        
        query = Vacante.query
        
        # Filtrar por estado si se proporciona
        if estado:
            query = query.filter_by(estado=estado)
        
        # Filtrar por avance si se proporciona
        if avance:
            query = query.filter_by(avance=avance)
        
        # ⭐ NUEVO - Filtrar por búsqueda en nombre de vacante
        if search:
            query = query.filter(Vacante.nombre.contains(search))
        
        # ⭐ NUEVO - Filtrar por cliente o CCP
        if cliente:
            from models import Cliente
            query = query.join(Cliente).filter(
                db.or_(
                    Cliente.nombre.contains(cliente),
                    Cliente.ccp.contains(cliente)
                )
            )
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.filter_by(reclutador_id=current_user.id)
        
        # Actualizar días transcurridos para todas las vacantes
        for vacante in query.all():
            vacante.dias_transcurridos = vacante.calcular_dias_transcurridos()
        db.session.commit()
        
        vacantes = query.order_by(Vacante.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'vacantes': [vacante.to_dict() for vacante in vacantes.items],
            'total': vacantes.total,
            'pages': vacantes.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo vacantes: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['GET'])
@token_required
def get_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver esta vacante'}), 403
        
        # Actualizar días transcurridos
        vacante.dias_transcurridos = vacante.calcular_dias_transcurridos()
        db.session.commit()
        
        # Incluir información detallada de candidatos
        vacante_dict = vacante.to_dict()
        
        # Agregar listas detalladas de candidatos
        vacante_dict['candidatos_detalle'] = []
        vacante_dict['en_entrevista_detalle'] = []
        vacante_dict['seleccionados_detalle'] = []
        
        for cp in vacante.candidatos_posiciones:
            candidato_info = {
                'id': cp.candidato.id,
                'nombre': cp.candidato.nombre,
                'email': cp.candidato.email,
                'status': cp.status,
                'fecha_asignacion': cp.fecha_asignacion.isoformat() if cp.fecha_asignacion else None,
                'fecha_envio_candidato': cp.fecha_envio_candidato.isoformat() if cp.fecha_envio_candidato else None,
                'fecha_entrevista_ejecutivo': cp.fecha_entrevista_ejecutivo.isoformat() if cp.fecha_entrevista_ejecutivo else None,
                'entrevista_definitiva': cp.entrevista_definitiva.isoformat() if cp.entrevista_definitiva else None,
                'es_seleccionado': cp.es_seleccionado,
                'es_propuesta': cp.es_propuesta,
                'nota': cp.nota
            }
            
            vacante_dict['candidatos_detalle'].append(candidato_info)
            
            if cp.status in ['en_entrevista', 'entrevista_programada']:
                vacante_dict['en_entrevista_detalle'].append(candidato_info)
            
            if cp.es_seleccionado:
                vacante_dict['seleccionados_detalle'].append(candidato_info)
        
        return jsonify(vacante_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo vacante: {str(e)}'}), 500

@vacante_bp.route('', methods=['POST'])
@role_required('ejecutivo', 'reclutador_lider')
def create_vacante(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'reclutador_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar que el reclutador existe
        reclutador = Usuario.query.get(data['reclutador_id'])
        if not reclutador or reclutador.rol not in ['reclutador', 'reclutador_lider']:
            return jsonify({'message': 'Reclutador inválido'}), 400
        
        # Si no se especifica reclutador líder, usar el usuario actual si es líder
        reclutador_lider_id = data.get('reclutador_lider_id')
        if not reclutador_lider_id and current_user.rol == 'reclutador_lider':
            reclutador_lider_id = current_user.id
        
        # ⭐ NUEVO - Validar cliente si se proporciona
        cliente_id = data.get('cliente_id')
        if cliente_id:
            from models import Cliente
            cliente = Cliente.query.get(cliente_id)
            if not cliente or not cliente.activo:
                return jsonify({'message': 'Cliente inválido o inactivo'}), 400
        
        nueva_vacante = Vacante(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            ejecutivo_id=current_user.id,
            reclutador_id=data['reclutador_id'],
            reclutador_lider_id=reclutador_lider_id,
            cliente_id=cliente_id,  # ⭐ NUEVO
            
            # Campos específicos del proceso de reclutamiento
            vacantes=data.get('vacantes', 1),
            candidatos_requeridos=data.get('candidatos_requeridos', 3),
            entrevistas_op=data.get('entrevistas_op', 3),
            avance=data.get('avance', 'Creada'),
            
            # Campos opcionales del proceso
            envio_candidatos_rh=datetime.fromisoformat(data['envio_candidatos_rh']) if data.get('envio_candidatos_rh') else None,
            resumen_ia=data.get('resumen_ia'),
            informacion_clave_ia=data.get('informacion_clave_ia'),
            
            # Campos originales (opcional)
            prioridad=data.get('prioridad', 'media'),
            salario_min=data.get('salario_min'),
            salario_max=data.get('salario_max'),
            ubicacion=data.get('ubicacion'),
            modalidad=data.get('modalidad'),
            fecha_limite=datetime.fromisoformat(data['fecha_limite']) if data.get('fecha_limite') else None,
            comentarios=data.get('comentarios')
        )
        
        db.session.add(nueva_vacante)
        db.session.commit()
        
        return jsonify({
            'message': 'Vacante creada exitosamente',
            'vacante': nueva_vacante.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando vacante: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['PUT'])
@token_required
def update_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol not in ['ejecutivo', 'reclutador_lider'] and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar esta vacante'}), 403
        
        data = request.get_json()
        
        # ⭐ NUEVO - Validar cliente si se está actualizando
        if 'cliente_id' in data:
            cliente_id = data['cliente_id']
            if cliente_id:
                from models import Cliente
                cliente = Cliente.query.get(cliente_id)
                if not cliente or not cliente.activo:
                    return jsonify({'message': 'Cliente inválido o inactivo'}), 400
            vacante.cliente_id = cliente_id
        
        # Actualizar campos permitidos del proceso de reclutamiento
        campos_proceso = [
            'nombre', 'descripcion', 'avance', 'vacantes', 'candidatos_requeridos',
            'entrevistas_op', 'resumen_ia', 'informacion_clave_ia'
        ]
        
        for campo in campos_proceso:
            if campo in data:
                setattr(vacante, campo, data[campo])
        
        # Campos de fecha
        if 'envio_candidatos_rh' in data and data['envio_candidatos_rh']:
            vacante.envio_candidatos_rh = datetime.fromisoformat(data['envio_candidatos_rh'])
        
        if 'fecha_limite' in data and data['fecha_limite']:
            vacante.fecha_limite = datetime.fromisoformat(data['fecha_limite'])
        
        # Campos originales (para compatibilidad)
        campos_originales = [
            'estado', 'prioridad', 'salario_min', 'salario_max', 
            'ubicacion', 'modalidad', 'comentarios'
        ]
        
        for campo in campos_originales:
            if campo in data:
                setattr(vacante, campo, data[campo])
        
        # Actualizar días transcurridos
        vacante.dias_transcurridos = vacante.calcular_dias_transcurridos()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Vacante actualizada exitosamente',
            'vacante': vacante.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando vacante: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['DELETE'])
@role_required('ejecutivo', 'reclutador_lider')
def delete_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Cambiar estado a cancelada en lugar de eliminar físicamente
        vacante.estado = 'cancelada'
        vacante.avance = 'Cancelada'
        db.session.commit()
        
        return jsonify({'message': 'Vacante cancelada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando vacante: {str(e)}'}), 500

# Nuevos endpoints específicos para el proceso de reclutamiento

@vacante_bp.route('/<int:vacante_id>/enviar-candidatos', methods=['POST'])
@role_required('reclutador', 'reclutador_lider')
def enviar_candidatos_rh(current_user, vacante_id):
    """Marcar cuando RH envía candidatos al ejecutivo"""
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para esta acción'}), 403
        
        data = request.get_json()
        candidatos_ids = data.get('candidatos_ids', [])
        
        if not candidatos_ids:
            return jsonify({'message': 'Se requiere al menos un candidato'}), 400
        
        # Actualizar fecha de envío en la vacante
        vacante.envio_candidatos_rh = datetime.utcnow()
        vacante.avance = 'Candidatos enviados a RH'
        
        # Actualizar fecha de envío para cada candidato
        from models import CandidatosPositions
        for candidato_id in candidatos_ids:
            cp = CandidatosPositions.query.filter_by(
                candidato_id=candidato_id, 
                vacante_id=vacante_id
            ).first()
            
            if cp:
                cp.fecha_envio_candidato = datetime.utcnow()
                cp.status = 'enviado_rh'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Candidatos enviados a RH exitosamente',
            'vacante': vacante.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error enviando candidatos: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>/programar-entrevista', methods=['POST'])
@token_required
def programar_entrevista_ejecutivo(current_user, vacante_id):
    """Programar entrevista con ejecutivo"""
    try:
        data = request.get_json()
        candidato_id = data.get('candidato_id')
        fecha_entrevista = data.get('fecha_entrevista')
        
        if not candidato_id or not fecha_entrevista:
            return jsonify({'message': 'candidato_id y fecha_entrevista son requeridos'}), 400
        
        from models import CandidatosPositions
        cp = CandidatosPositions.query.filter_by(
            candidato_id=candidato_id, 
            vacante_id=vacante_id
        ).first()
        
        if not cp:
            return jsonify({'message': 'Candidato no encontrado en esta vacante'}), 404
        
        cp.fecha_entrevista_ejecutivo = datetime.fromisoformat(fecha_entrevista)
        cp.status = 'entrevista_programada'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Entrevista programada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error programando entrevista: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>/seleccionar-candidato', methods=['POST'])
@token_required
def seleccionar_candidato(current_user, vacante_id):
    """Marcar candidato como seleccionado"""
    try:
        data = request.get_json()
        candidato_id = data.get('candidato_id')
        es_propuesta = data.get('es_propuesta', False)
        
        if not candidato_id:
            return jsonify({'message': 'candidato_id es requerido'}), 400
        
        from models import CandidatosPositions
        cp = CandidatosPositions.query.filter_by(
            candidato_id=candidato_id, 
            vacante_id=vacante_id
        ).first()
        
        if not cp:
            return jsonify({'message': 'Candidato no encontrado en esta vacante'}), 404
        
        cp.es_seleccionado = True
        cp.es_propuesta = es_propuesta
        cp.status = 'seleccionado'
        cp.entrevista_definitiva = datetime.utcnow()
        
        # Actualizar avance de la vacante
        vacante = Vacante.query.get(vacante_id)
        seleccionados_count = len(vacante.get_candidatos_seleccionados())
        
        if seleccionados_count >= vacante.vacantes:
            vacante.avance = 'Posiciones cubiertas'
            vacante.estado = 'cerrada'
        else:
            vacante.avance = f'Seleccionando candidatos ({seleccionados_count}/{vacante.vacantes})'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato seleccionado exitosamente',
            'vacante': vacante.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error seleccionando candidato: {str(e)}'}), 500

@vacante_bp.route('/dashboard-stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    """Obtener estadísticas para el dashboard similar al CSV"""
    try:
        # Filtrar vacantes según rol
        query = Vacante.query
        if current_user.rol == 'reclutador':
            query = query.filter_by(reclutador_id=current_user.id)
        
        vacantes = query.all()
        
        # Estadísticas generales
        stats = {
            'total_vacantes': len(vacantes),
            'vacantes_abiertas': len([v for v in vacantes if v.estado == 'abierta']),
            'vacantes_cerradas': len([v for v in vacantes if v.estado == 'cerrada']),
            'total_candidatos': sum([len(v.candidatos_posiciones) for v in vacantes]),
            'candidatos_seleccionados': sum([len(v.get_candidatos_seleccionados()) for v in vacantes]),
            'propuestas_totales': sum([v.get_propuestas_count() for v in vacantes]),
        }
        
        # Estadísticas por avance
        avances = {}
        for vacante in vacantes:
            avance = vacante.avance or 'Sin avance'
            if avance not in avances:
                avances[avance] = 0
            avances[avance] += 1
        
        stats['por_avance'] = avances
        
        # Vacantes más antiguas (más días transcurridos)
        vacantes_antiguas = sorted(vacantes, key=lambda v: v.calcular_dias_transcurridos(), reverse=True)[:5]
        stats['vacantes_antiguas'] = [
            {
                'id': v.id,
                'nombre': v.nombre,
                'dias_transcurridos': v.calcular_dias_transcurridos(),
                'ejecutivo': v.ejecutivo.nombre if v.ejecutivo else None,
                'candidatos': len(v.candidatos_posiciones)
            } for v in vacantes_antiguas
        ]
        
        # Reclutadores con más vacantes
        reclutadores_stats = {}
        for vacante in vacantes:
            reclutador = vacante.reclutador.nombre if vacante.reclutador else 'Sin asignar'
            if reclutador not in reclutadores_stats:
                reclutadores_stats[reclutador] = {
                    'vacantes': 0,
                    'candidatos': 0,
                    'seleccionados': 0
                }
            reclutadores_stats[reclutador]['vacantes'] += 1
            reclutadores_stats[reclutador]['candidatos'] += len(vacante.candidatos_posiciones)
            reclutadores_stats[reclutador]['seleccionados'] += len(vacante.get_candidatos_seleccionados())
        
        stats['por_reclutador'] = reclutadores_stats
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo estadísticas: {str(e)}'}), 500
