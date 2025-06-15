import axios from 'axios';

// Configuración base de Axios
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

console.log('🔗 API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos timeout (era 10 segundos)
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Log para debugging
    console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, {
      headers: config.headers,
      data: config.data
    });
    
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => {
    console.log(`✅ ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ Response error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      message: error.response?.data?.message || error.message,
      data: error.response?.data
    });
    
    if (error.response?.status === 401) {
      console.log('🔐 Token inválido, redirigiendo a login...');
      localStorage.removeItem('authToken');
      localStorage.removeItem('userInfo');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Función para probar la conexión con el backend
export const testConnection = async () => {
  try {
    const response = await api.get('/health');
    console.log('💚 Conexión con backend exitosa:', response.data);
    return { success: true, data: response.data };
  } catch (error) {
    console.error('💔 Error de conexión con backend:', error);
    return { 
      success: false, 
      error: error.response?.data?.message || error.message 
    };
  }
};

// Servicios de Autenticación
export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
  },
  // Nuevo: verificar si el token es válido
  verifyToken: async () => {
    try {
      const response = await api.get('/auth/verify');
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.response?.data?.message || error.message };
    }
  }
};

// Servicios de Usuarios
export const userService = {
  getUsers: (page = 1, perPage = 10) => api.get(`/usuarios?page=${page}&per_page=${perPage}`),
  getUser: (id) => api.get(`/usuarios/${id}`),
  createUser: (userData) => api.post('/usuarios', userData),
  updateUser: (id, userData) => api.put(`/usuarios/${id}`, userData),
  deleteUser: (id) => api.delete(`/usuarios/${id}`)
};

// Servicios de Vacantes
export const vacantService = {
  getVacants: (page = 1, perPage = 10, estado = null) => {
    let url = `/vacantes?page=${page}&per_page=${perPage}`;
    if (estado) url += `&estado=${estado}`;
    return api.get(url);
  },
  getVacant: (id) => api.get(`/vacantes/${id}`),
  createVacant: (vacantData) => api.post('/vacantes', vacantData),
  updateVacant: (id, vacantData) => api.put(`/vacantes/${id}`, vacantData),
  deleteVacant: (id) => api.delete(`/vacantes/${id}`),
  
  // Nuevos endpoints para el flujo real
  sendCandidatesHR: (vacanteId, data) => api.post(`/vacantes/${vacanteId}/enviar-candidatos`, data),
  scheduleInterview: (vacanteId, data) => api.post(`/vacantes/${vacanteId}/programar-entrevista`, data),
  selectCandidate: (vacanteId, data) => api.post(`/vacantes/${vacanteId}/seleccionar-candidato`, data),
  getDashboardStats: () => api.get('/vacantes/dashboard-stats')
};

// Servicios de Candidatos
export const candidateService = {
  getCandidates: (page = 1, perPage = 10, search = null, estado = null) => {
    let url = `/candidatos?page=${page}&per_page=${perPage}`;
    if (search) url += `&search=${search}`;
    if (estado) url += `&estado=${estado}`;
    return api.get(url);
  },
  getCandidate: (id) => api.get(`/candidatos/${id}`),
  createCandidate: (candidateData) => api.post('/candidatos', candidateData),
  updateCandidate: (id, candidateData) => api.put(`/candidatos/${id}`, candidateData),
  deleteCandidate: (id) => api.delete(`/candidatos/${id}`)
};

// Servicios de Documentos
export const documentService = {
  uploadDocument: (formData) => api.post('/documentos/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getDocument: (id) => api.get(`/documentos/${id}`),
  deleteDocument: (id) => api.delete(`/documentos/${id}`)
};

// Servicios de Entrevistas
export const interviewService = {
  getInterviews: (page = 1, perPage = 10, fechaDesde = null, fechaHasta = null) => {
    let url = `/entrevistas?page=${page}&per_page=${perPage}`;
    if (fechaDesde) url += `&fecha_desde=${fechaDesde}`;
    if (fechaHasta) url += `&fecha_hasta=${fechaHasta}`;
    return api.get(url);
  },
  getInterview: (id) => api.get(`/entrevistas/${id}`),
  createInterview: (interviewData) => api.post('/entrevistas', interviewData),
  updateInterview: (id, interviewData) => api.put(`/entrevistas/${id}`, interviewData),
  deleteInterview: (id) => api.delete(`/entrevistas/${id}`)
};

// Servicios de Candidatos-Posiciones
export const candidatePositionService = {
  getAssignments: (page = 1, perPage = 10, candidatoId = null, vacanteId = null, status = null) => {
    let url = `/candidatos-posiciones?page=${page}&per_page=${perPage}`;
    if (candidatoId) url += `&candidato_id=${candidatoId}`;
    if (vacanteId) url += `&vacante_id=${vacanteId}`;
    if (status) url += `&status=${status}`;
    return api.get(url);
  },
  createAssignment: (assignmentData) => api.post('/candidatos-posiciones', assignmentData),
  updateAssignment: (id, assignmentData) => api.put(`/candidatos-posiciones/${id}`, assignmentData),
  deleteAssignment: (id) => api.delete(`/candidatos-posiciones/${id}`),
  
  // Nuevos endpoints para el flujo real
  getCandidatesByVacant: (vacanteId) => api.get(`/candidatos-posiciones/por-vacante/${vacanteId}`),
  acceptBySupervisor: (assignmentId, data) => api.post(`/candidatos-posiciones/${assignmentId}/aceptar-supervisor`, data),
  finalizeProcess: (assignmentId, data) => api.post(`/candidatos-posiciones/${assignmentId}/finalizar-proceso`, data),
  getStatistics: () => api.get('/candidatos-posiciones/estadisticas')
};

// Servicios de Reportes
export const reportService = {
  getDashboardStats: () => {
    // Timeout específico para dashboard (puede ser lento)
    return api.get('/reports/dashboard', { timeout: 45000 }); // 45 segundos
  },
  getVacantReport: (vacanteId) => api.get(`/reports/vacante/${vacanteId}/reporte`)
};

// Función helper para manejar errores comunes
export const handleApiError = (error) => {
  if (error.response) {
    // Error del servidor
    return error.response.data?.message || `Error ${error.response.status}: ${error.response.statusText}`;
  } else if (error.request) {
    // Error de red
    return 'Error de conexión. Verifica tu conexión a internet.';
  } else {
    // Error de configuración
    return 'Error inesperado. Inténtalo de nuevo.';
  }
};

export default api;
