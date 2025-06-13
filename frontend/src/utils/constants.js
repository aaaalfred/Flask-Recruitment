// Estados de candidatos
export const CANDIDATE_STATES = {
  ACTIVO: 'activo',
  INACTIVO: 'inactivo',
  BLACKLIST: 'blacklist'
};

// Estados de vacantes
export const VACANT_STATES = {
  ABIERTA: 'abierta',
  PAUSADA: 'pausada',
  CERRADA: 'cerrada',
  CANCELADA: 'cancelada'
};

// Prioridades de vacantes
export const VACANT_PRIORITIES = {
  BAJA: 'baja',
  MEDIA: 'media',
  ALTA: 'alta',
  CRITICA: 'critica'
};

// Modalidades de trabajo
export const WORK_MODALITIES = {
  PRESENCIAL: 'presencial',
  REMOTO: 'remoto',
  HIBRIDO: 'hibrido'
};

// Disponibilidades
export const AVAILABILITIES = {
  INMEDIATA: 'inmediata',
  QUINCE_DIAS: '15_dias',
  TREINTA_DIAS: '30_dias',
  A_CONVENIR: 'a_convenir'
};

// Niveles de inglés
export const ENGLISH_LEVELS = {
  BASICO: 'basico',
  INTERMEDIO: 'intermedio',
  AVANZADO: 'avanzado',
  NATIVO: 'nativo'
};

// Tipos de entrevista
export const INTERVIEW_TYPES = {
  TELEFONICA: 'telefonica',
  VIDEO: 'video',
  PRESENCIAL: 'presencial',
  TECNICA: 'tecnica'
};

// Resultados de entrevista
export const INTERVIEW_RESULTS = {
  PENDIENTE: 'pendiente',
  APROBADA: 'aprobada',
  RECHAZADA: 'rechazada',
  REPROGRAMAR: 'reprogramar'
};

// Estados de candidatos en posiciones
export const POSITION_STATUSES = {
  POSTULADO: 'postulado',
  EN_PROCESO: 'en_proceso',
  SELECCIONADO: 'seleccionado',
  RECHAZADO: 'rechazado',
  RETIRADO: 'retirado'
};

// Roles de usuario
export const USER_ROLES = {
  EJECUTIVO: 'ejecutivo',
  RECLUTADOR: 'reclutador',
  RECLUTADOR_LIDER: 'reclutador_lider'
};

// Tipos de documento
export const DOCUMENT_TYPES = {
  CV: 'cv',
  CERTIFICADO: 'certificado',
  COMPROBANTE: 'comprobante',
  OTRO: 'otro'
};

// Labels en español para mostrar en la UI
export const LABELS = {
  CANDIDATE_STATES: {
    [CANDIDATE_STATES.ACTIVO]: 'Activo',
    [CANDIDATE_STATES.INACTIVO]: 'Inactivo',
    [CANDIDATE_STATES.BLACKLIST]: 'Lista Negra'
  },
  
  VACANT_STATES: {
    [VACANT_STATES.ABIERTA]: 'Abierta',
    [VACANT_STATES.PAUSADA]: 'Pausada',
    [VACANT_STATES.CERRADA]: 'Cerrada',
    [VACANT_STATES.CANCELADA]: 'Cancelada'
  },
  
  VACANT_PRIORITIES: {
    [VACANT_PRIORITIES.BAJA]: 'Baja',
    [VACANT_PRIORITIES.MEDIA]: 'Media',
    [VACANT_PRIORITIES.ALTA]: 'Alta',
    [VACANT_PRIORITIES.CRITICA]: 'Crítica'
  },
  
  WORK_MODALITIES: {
    [WORK_MODALITIES.PRESENCIAL]: 'Presencial',
    [WORK_MODALITIES.REMOTO]: 'Remoto',
    [WORK_MODALITIES.HIBRIDO]: 'Híbrido'
  },
  
  AVAILABILITIES: {
    [AVAILABILITIES.INMEDIATA]: 'Inmediata',
    [AVAILABILITIES.QUINCE_DIAS]: '15 días',
    [AVAILABILITIES.TREINTA_DIAS]: '30 días',
    [AVAILABILITIES.A_CONVENIR]: 'A convenir'
  },
  
  ENGLISH_LEVELS: {
    [ENGLISH_LEVELS.BASICO]: 'Básico',
    [ENGLISH_LEVELS.INTERMEDIO]: 'Intermedio',
    [ENGLISH_LEVELS.AVANZADO]: 'Avanzado',
    [ENGLISH_LEVELS.NATIVO]: 'Nativo'
  },
  
  INTERVIEW_TYPES: {
    [INTERVIEW_TYPES.TELEFONICA]: 'Telefónica',
    [INTERVIEW_TYPES.VIDEO]: 'Video',
    [INTERVIEW_TYPES.PRESENCIAL]: 'Presencial',
    [INTERVIEW_TYPES.TECNICA]: 'Técnica'
  },
  
  INTERVIEW_RESULTS: {
    [INTERVIEW_RESULTS.PENDIENTE]: 'Pendiente',
    [INTERVIEW_RESULTS.APROBADA]: 'Aprobada',
    [INTERVIEW_RESULTS.RECHAZADA]: 'Rechazada',
    [INTERVIEW_RESULTS.REPROGRAMAR]: 'Reprogramar'
  },
  
  POSITION_STATUSES: {
    [POSITION_STATUSES.POSTULADO]: 'Postulado',
    [POSITION_STATUSES.EN_PROCESO]: 'En Proceso',
    [POSITION_STATUSES.SELECCIONADO]: 'Seleccionado',
    [POSITION_STATUSES.RECHAZADO]: 'Rechazado',
    [POSITION_STATUSES.RETIRADO]: 'Retirado'
  },
  
  USER_ROLES: {
    [USER_ROLES.EJECUTIVO]: 'Ejecutivo',
    [USER_ROLES.RECLUTADOR]: 'Reclutador',
    [USER_ROLES.RECLUTADOR_LIDER]: 'Reclutador Líder'
  },
  
  DOCUMENT_TYPES: {
    [DOCUMENT_TYPES.CV]: 'CV',
    [DOCUMENT_TYPES.CERTIFICADO]: 'Certificado',
    [DOCUMENT_TYPES.COMPROBANTE]: 'Comprobante',
    [DOCUMENT_TYPES.OTRO]: 'Otro'
  }
};

// Colores para badges según el estado
export const STATUS_COLORS = {
  CANDIDATE_STATES: {
    [CANDIDATE_STATES.ACTIVO]: 'badge-success',
    [CANDIDATE_STATES.INACTIVO]: 'badge-warning',
    [CANDIDATE_STATES.BLACKLIST]: 'badge-danger'
  },
  
  VACANT_STATES: {
    [VACANT_STATES.ABIERTA]: 'badge-success',
    [VACANT_STATES.PAUSADA]: 'badge-warning',
    [VACANT_STATES.CERRADA]: 'badge-primary',
    [VACANT_STATES.CANCELADA]: 'badge-danger'
  },
  
  VACANT_PRIORITIES: {
    [VACANT_PRIORITIES.BAJA]: 'badge-primary',
    [VACANT_PRIORITIES.MEDIA]: 'badge-warning',
    [VACANT_PRIORITIES.ALTA]: 'bg-orange-100 text-orange-800',
    [VACANT_PRIORITIES.CRITICA]: 'badge-danger'
  },
  
  INTERVIEW_RESULTS: {
    [INTERVIEW_RESULTS.PENDIENTE]: 'badge-warning',
    [INTERVIEW_RESULTS.APROBADA]: 'badge-success',
    [INTERVIEW_RESULTS.RECHAZADA]: 'badge-danger',
    [INTERVIEW_RESULTS.REPROGRAMAR]: 'bg-blue-100 text-blue-800'
  },
  
  POSITION_STATUSES: {
    [POSITION_STATUSES.POSTULADO]: 'badge-primary',
    [POSITION_STATUSES.EN_PROCESO]: 'badge-warning',
    [POSITION_STATUSES.SELECCIONADO]: 'badge-success',
    [POSITION_STATUSES.RECHAZADO]: 'badge-danger',
    [POSITION_STATUSES.RETIRADO]: 'bg-gray-100 text-gray-800'
  }
};

// Configuración de paginación
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [5, 10, 20, 50, 100]
};

// Rutas de la aplicación
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  DASHBOARD: '/dashboard',
  VACANTS: '/vacants',
  CANDIDATES: '/candidates',
  INTERVIEWS: '/interviews',
  USERS: '/users',
  REPORTS: '/reports',
  PROFILE: '/profile'
};

// Configuración de archivos
export const FILE_CONFIG = {
  MAX_SIZE: 16 * 1024 * 1024, // 16MB
  ALLOWED_TYPES: ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'],
  ACCEPTED_MIME_TYPES: [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'image/jpeg',
    'image/jpg',
    'image/png'
  ]
};

// Mensajes de error comunes
export const ERROR_MESSAGES = {
  REQUIRED_FIELD: 'Este campo es requerido',
  INVALID_EMAIL: 'Ingresa un email válido',
  INVALID_PHONE: 'Ingresa un teléfono válido',
  PASSWORD_TOO_SHORT: 'La contraseña debe tener al menos 6 caracteres',
  PASSWORDS_NOT_MATCH: 'Las contraseñas no coinciden',
  FILE_TOO_LARGE: 'El archivo es demasiado grande',
  INVALID_FILE_TYPE: 'Tipo de archivo no permitido',
  NETWORK_ERROR: 'Error de conexión. Verifica tu conexión a internet.',
  UNAUTHORIZED: 'No tienes permisos para realizar esta acción',
  NOT_FOUND: 'El recurso solicitado no fue encontrado',
  SERVER_ERROR: 'Error interno del servidor. Intenta nuevamente.'
};

// Mensajes de éxito
export const SUCCESS_MESSAGES = {
  CREATED: 'Creado exitosamente',
  UPDATED: 'Actualizado exitosamente',
  DELETED: 'Eliminado exitosamente',
  LOGIN: 'Inicio de sesión exitoso',
  LOGOUT: 'Sesión cerrada exitosamente',
  FILE_UPLOADED: 'Archivo subido exitosamente',
  EMAIL_SENT: 'Email enviado exitosamente'
};
