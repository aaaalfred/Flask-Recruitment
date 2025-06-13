from extensions import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia para relación muchos a muchos
class CandidatosPositions(db.Model):
    __tablename__ = 'candidatos_posiciones'
    
    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='postulado')
    nota = db.Column(db.Text)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidato = db.relationship('Candidato', backref='posiciones_rel', overlaps="candidato,candidatos_posiciones")
    vacante = db.relationship('Vacante', backref='candidatos_rel', overlaps="vacante,candidatos_posiciones")

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
    vacantes_ejecutivo = db.relationship('Vacante', foreign_keys='Vacante.ejecutivo_id', backref='ejecutivo')
    vacantes_reclutador = db.relationship('Vacante', foreign_keys='Vacante.reclutador_id', backref='reclutador')
    vacantes_lider = db.relationship('Vacante', foreign_keys='Vacante.reclutador_lider_id', backref='reclutador_lider')
    candidatos = db.relationship('Candidato', backref='reclutador_asignado')
    
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
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    ejecutivo_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    vacantes = db.Column(db.Integer, default=1)
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
    
    # Relationships
    entrevistas = db.relationship('Entrevista', backref='vacante_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', backref='vacante_rel', cascade='all, delete-orphan', overlaps="candidatos_rel,vacante")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            'ejecutivo_id': self.ejecutivo_id,
            'reclutador_id': self.reclutador_id,
            'reclutador_lider_id': self.reclutador_lider_id,
            'vacantes': self.vacantes,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'salario_min': float(self.salario_min) if self.salario_min else None,
            'salario_max': float(self.salario_max) if self.salario_max else None,
            'ubicacion': self.ubicacion,
            'modalidad': self.modalidad,
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'comentarios': self.comentarios,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
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
    cv_url = db.Column(db.String(500))
    estado = db.Column(db.Enum('activo', 'inactivo', 'blacklist'), default='activo')
    comentarios_finales = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    salario_esperado = db.Column(db.Numeric(10, 2))
    experiencia_anos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(100))
    disponibilidad = db.Column(db.Enum('inmediata', '15_dias', '30_dias', 'a_convenir'))
    nivel_ingles = db.Column(db.Enum('basico', 'intermedio', 'avanzado', 'nativo'))
    linkedin_url = db.Column(db.String(200))
    
    # Relationships
    documentos = db.relationship('Documento', backref='candidato_rel', cascade='all, delete-orphan')
    entrevistas = db.relationship('Entrevista', backref='candidato_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', backref='candidato_rel', cascade='all, delete-orphan', overlaps="candidato,posiciones_rel")
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'cv_url': self.cv_url,
            'estado': self.estado,
            'comentarios_finales': self.comentarios_finales,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'reclutador_id': self.reclutador_id,
            'salario_esperado': float(self.salario_esperado) if self.salario_esperado else None,
            'experiencia_anos': self.experiencia_anos,
            'ubicacion': self.ubicacion,
            'disponibilidad': self.disponibilidad,
            'nivel_ingles': self.nivel_ingles,
            'linkedin_url': self.linkedin_url,
            'reclutador': self.reclutador_asignado.nombre if self.reclutador_asignado else None
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
    tipo = db.Column(db.Enum('telefonica', 'video', 'presencial', 'tecnica'), nullable=False)
    resultado = db.Column(db.Enum('pendiente', 'aprobada', 'rechazada', 'reprogramar'), default='pendiente')
    comentarios = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)  # 1-10
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    entrevistador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    duracion_minutos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(200))  # Para presenciales o link para video
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    entrevistador = db.relationship('Usuario', backref='entrevistas_realizadas')
    
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
