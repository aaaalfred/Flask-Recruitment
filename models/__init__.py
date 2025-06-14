from extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia para relación muchos a muchos - ACTUALIZADA CON CAMPOS REALES
class CandidatosPositions(db.Model):
    __tablename__ = 'candidatos_posiciones'
    
    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    
    # Campos del proceso real de evaluación
    status = db.Column(db.String(50), nullable=False, default='postulado')  # postulado, en_proceso, rechazado, aceptado, contratado
    aceptado = db.Column(db.Boolean, default=False)  # Si fue aceptado por supervisor
    contratado_status = db.Column(db.Enum('pendiente', 'rechazado', 'contratado', 'no_contratable'), default='pendiente')
    
    # Comentarios y notas del proceso
    comentarios_finales = db.Column(db.Text)  # Razón de rechazo/aceptación
    nota_reclutador = db.Column(db.Text)  # Notas internas del reclutador
    
    # Archivos específicos para esta aplicación
    archivo_cv = db.Column(db.String(200))  # Nombre del archivo CV para esta vacante específica
    cv_url_especifico = db.Column(db.String(500))  # URL del CV específico para esta vacante
    
    # Fechas del proceso
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_envio_candidato = db.Column(db.DateTime)  # Cuándo se envió al ejecutivo
    fecha_entrevista_ejecutivo = db.Column(db.DateTime)  # Cuándo fue la entrevista
    fecha_decision_final = db.Column(db.DateTime)  # Cuándo se tomó la decisión final
    
    # Estados adicionales del flujo
    entrevista_realizada = db.Column(db.Boolean, default=False)
    se_presento = db.Column(db.Boolean, default=True)  # Si se presentó a las citas/tienda
    motivo_rechazo = db.Column(db.String(200))  # Motivo específico de rechazo
    
    # Relationships
    candidato = db.relationship('Candidato', back_populates='candidatos_posiciones')
    vacante = db.relationship('Vacante', back_populates='candidatos_posiciones')
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidato_id': self.candidato_id,
            'vacante_id': self.vacante_id,
            'status': self.status,
            'aceptado': self.aceptado,
            'contratado_status': self.contratado_status,
            'comentarios_finales': self.comentarios_finales,
            'nota_reclutador': self.nota_reclutador,
            'archivo_cv': self.archivo_cv,
            'cv_url_especifico': self.cv_url_especifico,
            'fecha_asignacion': self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'fecha_envio_candidato': self.fecha_envio_candidato.isoformat() if self.fecha_envio_candidato else None,
            'fecha_entrevista_ejecutivo': self.fecha_entrevista_ejecutivo.isoformat() if self.fecha_entrevista_ejecutivo else None,
            'fecha_decision_final': self.fecha_decision_final.isoformat() if self.fecha_decision_final else None,
            'entrevista_realizada': self.entrevista_realizada,
            'se_presento': self.se_presento,
            'motivo_rechazo': self.motivo_rechazo,
            'candidato_nombre': self.candidato.nombre if self.candidato else None,
            'vacante_nombre': self.vacante.nombre if self.vacante else None
        }

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('ejecutivo', 'reclutador', 'reclutador_lider'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    vacantes_ejecutivo = db.relationship('Vacante', foreign_keys='Vacante.ejecutivo_id', back_populates='ejecutivo')
    vacantes_reclutador = db.relationship('Vacante', foreign_keys='Vacante.reclutador_id', back_populates='reclutador')
    vacantes_lider = db.relationship('Vacante', foreign_keys='Vacante.reclutador_lider_id', back_populates='reclutador_lider')
    candidatos = db.relationship('Candidato', back_populates='reclutador_asignado')
    entrevistas_realizadas = db.relationship('Entrevista', back_populates='entrevistador')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Vacante(db.Model):
    __tablename__ = 'vacante'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Campos básicos
    nombre = db.Column(db.String(200), nullable=False)  # Ej: "#2120 ACC CANCUN"
    descripcion = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    
    # IDs de usuarios
    ejecutivo_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    
    # Campos específicos del proceso de reclutamiento
    vacantes = db.Column(db.Integer, default=1)  # Número de posiciones
    candidatos_requeridos = db.Column(db.Integer, default=3)  # Candidatos que se necesitan presentar
    entrevistas_op = db.Column(db.Integer, default=3)  # Número de entrevistas operativas
    avance = db.Column(db.String(100))  # Estado del avance
    
    # Estados finales de la vacante
    status_final = db.Column(db.Enum('abierta', 'cubierta', 'cancelada', 'pausada'), default='abierta')
    
    # Fechas del proceso
    envio_candidatos_rh = db.Column(db.DateTime)  # Cuándo RH envía candidatos
    fecha_cierre = db.Column(db.DateTime)  # Cuándo se cierra la vacante
    
    # Contadores automáticos (se calculan dinámicamente)
    dias_transcurridos = db.Column(db.Integer, default=0)  # Días desde solicitud
    
    # Campos de IA y resumen
    resumen_ia = db.Column(db.Text)  # Resumen generado por IA
    informacion_clave_ia = db.Column(db.Text)  # Información clave extraída por IA
    
    # Campos originales que mantenemos por compatibilidad
    estado = db.Column(db.Enum('abierta', 'pausada', 'cerrada', 'cancelada'), default='abierta')
    prioridad = db.Column(db.Enum('baja', 'media', 'alta', 'critica'), default='media')
    salario_min = db.Column(db.Numeric(10, 2))
    salario_max = db.Column(db.Numeric(10, 2))
    ubicacion = db.Column(db.String(100))
    modalidad = db.Column(db.Enum('presencial', 'remoto', 'hibrido'))
    fecha_limite = db.Column(db.DateTime)
    comentarios = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships corregidas
    ejecutivo = db.relationship('Usuario', foreign_keys=[ejecutivo_id], back_populates='vacantes_ejecutivo')
    reclutador = db.relationship('Usuario', foreign_keys=[reclutador_id], back_populates='vacantes_reclutador')
    reclutador_lider = db.relationship('Usuario', foreign_keys=[reclutador_lider_id], back_populates='vacantes_lider')
    entrevistas = db.relationship('Entrevista', back_populates='vacante_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', back_populates='vacante', cascade='all, delete-orphan')
    
    def calcular_dias_transcurridos(self):
        """Calcular días transcurridos desde la fecha de solicitud"""
        if self.fecha_solicitud:
            delta = datetime.utcnow() - self.fecha_solicitud
            return delta.days
        return 0
    
    def get_candidatos_por_status(self, status):
        """Obtener candidatos por status específico"""
        return [cp for cp in self.candidatos_posiciones if cp.status == status]
    
    def get_candidatos_aceptados(self):
        """Obtener candidatos aceptados por supervisor"""
        return [cp for cp in self.candidatos_posiciones if cp.aceptado]
    
    def get_candidatos_contratados(self):
        """Obtener candidatos contratados"""
        return [cp for cp in self.candidatos_posiciones if cp.contratado_status == 'contratado']
    
    def get_candidatos_rechazados(self):
        """Obtener candidatos rechazados"""
        return [cp for cp in self.candidatos_posiciones if cp.contratado_status == 'rechazado']
    
    def get_candidatos_no_contratables(self):
        """Obtener candidatos marcados como no contratables"""
        return [cp for cp in self.candidatos_posiciones if cp.contratado_status == 'no_contratable']
    
    def actualizar_status_final(self):
        """Actualizar el status final basado en el estado de candidatos"""
        contratados = len(self.get_candidatos_contratados())
        if contratados >= self.vacantes:
            self.status_final = 'cubierta'
            self.avance = 'Posiciones cubiertas'
            self.fecha_cierre = datetime.utcnow()
    
    def get_candidatos_restantes(self):
        """Calcular candidatos restantes que se necesitan"""
        candidatos_actuales = len(self.candidatos_posiciones)
        return max(0, self.candidatos_requeridos - candidatos_actuales)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            'ejecutivo_id': self.ejecutivo_id,
            'reclutador_id': self.reclutador_id,
            'reclutador_lider_id': self.reclutador_lider_id,
            
            # Campos específicos del proceso
            'vacantes': self.vacantes,
            'candidatos_requeridos': self.candidatos_requeridos,
            'entrevistas_op': self.entrevistas_op,
            'avance': self.avance,
            'status_final': self.status_final,
            'dias_transcurridos': self.calcular_dias_transcurridos(),
            'envio_candidatos_rh': self.envio_candidatos_rh.isoformat() if self.envio_candidatos_rh else None,
            'fecha_cierre': self.fecha_cierre.isoformat() if self.fecha_cierre else None,
            'resumen_ia': self.resumen_ia,
            'informacion_clave_ia': self.informacion_clave_ia,
            
            # Contadores dinámicos basados en el estado real
            'total_candidatos': len(self.candidatos_posiciones),
            'candidatos_aceptados': len(self.get_candidatos_aceptados()),
            'candidatos_contratados': len(self.get_candidatos_contratados()),
            'candidatos_rechazados': len(self.get_candidatos_rechazados()),
            'candidatos_no_contratables': len(self.get_candidatos_no_contratables()),
            'candidatos_restantes': self.get_candidatos_restantes(),
            
            # Campos originales
            'estado': self.estado,
            'prioridad': self.prioridad,
            'salario_min': float(self.salario_min) if self.salario_min else None,
            'salario_max': float(self.salario_max) if self.salario_max else None,
            'ubicacion': self.ubicacion,
            'modalidad': self.modalidad,
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'comentarios': self.comentarios,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            
            # Nombres de usuarios
            'ejecutivo': self.ejecutivo.nombre if self.ejecutivo else None,
            'reclutador': self.reclutador.nombre if self.reclutador else None,
            'reclutador_lider': self.reclutador_lider.nombre if self.reclutador_lider else None
        }

class Candidato(db.Model):
    __tablename__ = 'candidato'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    
    # CV principal del candidato
    cv_url = db.Column(db.String(500))
    
    # Estado general del candidato
    estado = db.Column(db.Enum('activo', 'inactivo', 'blacklist'), default='activo')
    
    # Información del candidato
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    salario_esperado = db.Column(db.Numeric(10, 2))
    experiencia_anos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(100))
    disponibilidad = db.Column(db.Enum('inmediata', '15_dias', '30_dias', 'a_convenir'))
    nivel_ingles = db.Column(db.Enum('basico', 'intermedio', 'avanzado', 'nativo'))
    linkedin_url = db.Column(db.String(200))
    
    # Comentarios generales (no específicos de vacante)
    comentarios_generales = db.Column(db.Text)
    
    # Relationships
    reclutador_asignado = db.relationship('Usuario', back_populates='candidatos')
    documentos = db.relationship('Documento', back_populates='candidato_rel', cascade='all, delete-orphan')
    entrevistas = db.relationship('Entrevista', back_populates='candidato_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', back_populates='candidato', cascade='all, delete-orphan')
    
    def get_vacantes_aplicadas(self):
        """Obtener vacantes a las que ha aplicado"""
        return [cp.vacante for cp in self.candidatos_posiciones]
    
    def get_status_en_vacante(self, vacante_id):
        """Obtener status del candidato en una vacante específica"""
        cp = next((cp for cp in self.candidatos_posiciones if cp.vacante_id == vacante_id), None)
        return cp.status if cp else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'cv_url': self.cv_url,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'reclutador_id': self.reclutador_id,
            'salario_esperado': float(self.salario_esperado) if self.salario_esperado else None,
            'experiencia_anos': self.experiencia_anos,
            'ubicacion': self.ubicacion,
            'disponibilidad': self.disponibilidad,
            'nivel_ingles': self.nivel_ingles,
            'linkedin_url': self.linkedin_url,
            'comentarios_generales': self.comentarios_generales,
            'reclutador': self.reclutador_asignado.nombre if self.reclutador_asignado else None,
            'total_aplicaciones': len(self.candidatos_posiciones),
            'vacantes_aplicadas': [cp.vacante.nombre for cp in self.candidatos_posiciones]
        }

class Documento(db.Model):
    __tablename__ = 'documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_original = db.Column(db.String(200), nullable=False)
    url_s3 = db.Column(db.String(500), nullable=False)
    key_s3 = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.Enum('cv', 'certificado', 'comprobante', 'otro'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    tamaño_bytes = db.Column(db.Integer)
    content_type = db.Column(db.String(100))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    candidato_rel = db.relationship('Candidato', back_populates='documentos')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_original': self.nombre_original,
            'url_s3': self.url_s3,
            'tipo': self.tipo,
            'candidato_id': self.candidato_id,
            'tamaño_bytes': self.tamaño_bytes,
            'content_type': self.content_type,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None
        }

class Entrevista(db.Model):
    __tablename__ = 'entrevista'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.Enum('telefonica', 'video', 'presencial', 'tecnica', 'operativa', 'definitiva'), nullable=False)
    resultado = db.Column(db.Enum('pendiente', 'aprobada', 'rechazada', 'reprogramar'), default='pendiente')
    comentarios = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)  # 1-10
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    entrevistador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    duracion_minutos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(200))  # Para presenciales o link para video
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships corregidas
    candidato_rel = db.relationship('Candidato', back_populates='entrevistas')
    vacante_rel = db.relationship('Vacante', back_populates='entrevistas')
    entrevistador = db.relationship('Usuario', back_populates='entrevistas_realizadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'tipo': self.tipo,
            'resultado': self.resultado,
            'comentarios': self.comentarios,
            'puntuacion': self.puntuacion,
            'candidato_id': self.candidato_id,
            'vacante_id': self.vacante_id,
            'entrevistador_id': self.entrevistador_id,
            'duracion_minutos': self.duracion_minutos,
            'ubicacion': self.ubicacion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'candidato': self.candidato_rel.nombre if self.candidato_rel else None,
            'vacante': self.vacante_rel.nombre if self.vacante_rel else None,
            'entrevistador': self.entrevistador.nombre if self.entrevistador else None
        }
