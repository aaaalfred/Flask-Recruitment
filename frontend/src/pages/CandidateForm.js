import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  UserIcon,
  PhoneIcon,
  EnvelopeIcon,
  MapPinIcon,
  CurrencyDollarIcon,
  CalendarIcon,
  GlobeAltIcon,
  BuildingOfficeIcon,
  DocumentTextIcon,
  LinkIcon,
  CheckCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { candidateService, vacantService } from '../services/api';
import { LABELS } from '../utils/constants';
import toast from 'react-hot-toast';

const CandidateForm = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditing = Boolean(id);

  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [vacantes, setVacantes] = useState([]);
  
  const [formData, setFormData] = useState({
    nombre: '',
    telefono: '',
    email: '',
    ubicacion: '',
    experiencia_anos: '',
    salario_esperado: '',
    disponibilidad: '',
    nivel_ingles: '',
    linkedin_url: '',
    comentarios_finales: '',
    // Campos adicionales para edición
    estado: 'activo'
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (isEditing) {
      fetchCandidate();
    }
    fetchVacantes();
  }, [id, isEditing]);

  const fetchCandidate = async () => {
    try {
      setLoading(true);
      const response = await candidateService.getCandidate(id);
      const candidate = response.data;
      
      setFormData({
        nombre: candidate.nombre || '',
        telefono: candidate.telefono || '',
        email: candidate.email || '',
        ubicacion: candidate.ubicacion || '',
        experiencia_anos: candidate.experiencia_anos || '',
        salario_esperado: candidate.salario_esperado || '',
        disponibilidad: candidate.disponibilidad || '',
        nivel_ingles: candidate.nivel_ingles || '',
        linkedin_url: candidate.linkedin_url || '',
        comentarios_finales: candidate.comentarios_finales || '',
        estado: candidate.estado || 'activo'
      });
    } catch (error) {
      toast.error('Error al cargar los datos del candidato');
      navigate('/candidates');
    } finally {
      setLoading(false);
    }
  };

  const fetchVacantes = async () => {
    try {
      const response = await vacantService.getVacants(1, 100, 'abierta');
      setVacantes(response.data.vacantes || []);
    } catch (error) {
      console.error('Error fetching vacantes:', error);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.nombre.trim()) {
      newErrors.nombre = 'El nombre es requerido';
    }

    if (!formData.telefono.trim()) {
      newErrors.telefono = 'El teléfono es requerido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Por favor corrige los errores en el formulario');
      return;
    }

    try {
      setSaving(true);
      
      const dataToSend = { ...formData };
      
      // Si el email está vacío, no lo enviamos
      if (!dataToSend.email || dataToSend.email.trim() === '') {
        delete dataToSend.email;
      }

      if (isEditing) {
        await candidateService.updateCandidate(id, dataToSend);
        toast.success('Candidato actualizado exitosamente');
      } else {
        await candidateService.createCandidate(dataToSend);
        toast.success('Candidato creado exitosamente');
      }
      
      navigate('/candidates');
    } catch (error) {
      const message = error.response?.data?.message || 'Error al guardar el candidato';
      toast.error(message);
    } finally {
      setSaving(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Limpiar error del campo cuando el usuario comience a escribir
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {isEditing ? '✏️ Editar Candidato' : '👤 Nuevo Candidato'}
          </h1>
          <p className="mt-2 text-sm text-gray-700">
            {isEditing 
              ? 'Actualiza la información del candidato'
              : 'Completa la información básica del candidato'
            }
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            type="button"
            onClick={() => navigate('/candidates')}
            className="btn-secondary inline-flex items-center"
          >
            <XMarkIcon className="h-5 w-5 mr-2" />
            Cancelar
          </button>
        </div>
      </div>

      {/* Formulario */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Información Básica */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <UserIcon className="h-5 w-5 mr-2 text-primary-600" />
              Información Básica
            </h3>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              {/* Nombre Completo */}
              <div>
                <label className="form-label required">
                  Nombre Completo
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <UserIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    className={`form-input pl-10 ${errors.nombre ? 'border-red-300' : ''}`}
                    placeholder="Ej: Juan Pérez García"
                    value={formData.nombre}
                    onChange={(e) => handleInputChange('nombre', e.target.value)}
                  />
                </div>
                {errors.nombre && (
                  <p className="text-sm text-red-600 mt-1">{errors.nombre}</p>
                )}
              </div>

              {/* Teléfono */}
              <div>
                <label className="form-label required">
                  Teléfono
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <PhoneIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="tel"
                    className={`form-input pl-10 ${errors.telefono ? 'border-red-300' : ''}`}
                    placeholder="Ej: +52 55 1234 5678"
                    value={formData.telefono}
                    onChange={(e) => handleInputChange('telefono', e.target.value)}
                  />
                </div>
                {errors.telefono && (
                  <p className="text-sm text-red-600 mt-1">{errors.telefono}</p>
                )}
              </div>

              {/* Ubicación */}
              <div>
                <label className="form-label">
                  Ubicación
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <MapPinIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    className="form-input pl-10"
                    placeholder="Ej: Ciudad de México, México"
                    value={formData.ubicacion}
                    onChange={(e) => handleInputChange('ubicacion', e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Información Profesional */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <BuildingOfficeIcon className="h-5 w-5 mr-2 text-primary-600" />
              Información Profesional
            </h3>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              {/* Años de Experiencia */}
              <div>
                <label className="form-label">
                  Años de Experiencia
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  className="form-input"
                  placeholder="Ej: 5"
                  value={formData.experiencia_anos}
                  onChange={(e) => handleInputChange('experiencia_anos', e.target.value)}
                />
              </div>

              {/* Salario Esperado */}
              <div>
                <label className="form-label">
                  Salario Esperado (MXN)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <CurrencyDollarIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="number"
                    min="0"
                    step="1000"
                    className="form-input pl-10"
                    placeholder="Ej: 50000"
                    value={formData.salario_esperado}
                    onChange={(e) => handleInputChange('salario_esperado', e.target.value)}
                  />
                </div>
              </div>

              {/* Disponibilidad */}
              <div>
                <label className="form-label">
                  Disponibilidad
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <CalendarIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <select
                    className="form-input pl-10"
                    value={formData.disponibilidad}
                    onChange={(e) => handleInputChange('disponibilidad', e.target.value)}
                  >
                    <option value="">Seleccionar disponibilidad</option>
                    {Object.entries(LABELS.AVAILABILITY || {}).map(([key, label]) => (
                      <option key={key} value={key}>{label}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Nivel de Inglés */}
              <div>
                <label className="form-label">
                  Nivel de Inglés
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <GlobeAltIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <select
                    className="form-input pl-10"
                    value={formData.nivel_ingles}
                    onChange={(e) => handleInputChange('nivel_ingles', e.target.value)}
                  >
                    <option value="">Seleccionar nivel</option>
                    {Object.entries(LABELS.ENGLISH_LEVELS || {}).map(([key, label]) => (
                      <option key={key} value={key}>{label}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* LinkedIn */}
              <div className="sm:col-span-2">
                <label className="form-label">
                  LinkedIn Profile
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <LinkIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="url"
                    className="form-input pl-10"
                    placeholder="https://linkedin.com/in/usuario"
                    value={formData.linkedin_url}
                    onChange={(e) => handleInputChange('linkedin_url', e.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Estado (solo para edición) */}
          {isEditing && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <CheckCircleIcon className="h-5 w-5 mr-2 text-primary-600" />
                Estado del Candidato
              </h3>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label className="form-label">
                    Estado
                  </label>
                  <select
                    className="form-input"
                    value={formData.estado}
                    onChange={(e) => handleInputChange('estado', e.target.value)}
                  >
                    {Object.entries(LABELS.CANDIDATE_STATES || {}).map(([key, label]) => (
                      <option key={key} value={key}>{label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Comentarios */}
          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <DocumentTextIcon className="h-5 w-5 mr-2 text-primary-600" />
              Comentarios Adicionales
            </h3>
            <div>
              <label className="form-label">
                Comentarios y Observaciones
              </label>
              <textarea
                rows={4}
                className="form-input"
                placeholder="Información adicional sobre el candidato, habilidades destacadas, experiencia relevante, etc."
                value={formData.comentarios_finales}
                onChange={(e) => handleInputChange('comentarios_finales', e.target.value)}
              />
            </div>
          </div>

          {/* Botones */}
          <div className="flex justify-end space-x-3 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={() => navigate('/candidates')}
              className="btn-secondary"
              disabled={saving}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={saving}
              className="btn-primary inline-flex items-center"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {isEditing ? 'Actualizando...' : 'Creando...'}
                </>
              ) : (
                <>
                  <CheckCircleIcon className="h-5 w-5 mr-2" />
                  {isEditing ? 'Actualizar Candidato' : 'Crear Candidato'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CandidateForm;
