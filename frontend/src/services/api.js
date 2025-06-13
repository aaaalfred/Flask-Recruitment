import axios from 'axios';

// Configuración base de Axios
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token automáticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userInfo');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios de Autenticación
export const authService = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
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
  deleteVacant: (id) => api.delete(`/vacantes/${id}`)
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
  deleteAssignment: (id) => api.delete(`/candidatos-posiciones/${id}`)
};

// Servicios de Reportes
export const reportService = {
  getDashboardStats: () => api.get('/reports/dashboard'),
  getVacantReport: (vacanteId) => api.get(`/reports/vacante/${vacanteId}/reporte`)
};

export default api;
