import React, { useState, useEffect } from 'react';
import {
  XMarkIcon,
  UserIcon,
  PhoneIcon,
  DocumentTextIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { candidateService } from '../services/api';
import { LABELS } from '../utils/constants';
import toast from 'react-hot-toast';

const CandidateModal = ({ isOpen, onClose, candidate = null, onSave }) => {
  const isEditing = Boolean(candidate);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  
  const [formData, setFormData] = useState({
    nombre: '',
    telefono: '',
    comentarios_finales: '',
    estado: 'activo'
  });

  const [errors, setErrors] = useState({});

  // Resetear formulario cuando se abre/cierra el modal
  useEffect(() => {
    if (isOpen) {
      if (candidate) {
        setFormData({
          nombre: candidate.nombre || '',
          telefono: candidate.telefono || '',
          comentarios_finales: candidate.comentarios_finales || candidate.comentarios_generales || '',
          estado: candidate.estado || 'activo'
        });
      } else {
        setFormData({
          nombre: '',
          telefono: '',
          comentarios_finales: '',
          estado: 'activo'
        });
      }
      setErrors({});
    }
  }, [isOpen, candidate]);

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
      
      // Limpiar campos vacíos opcionales
      if (!dataToSend.comentarios_finales.trim()) {
        delete dataToSend.comentarios_finales;
      }

      let response;
      if (isEditing) {
        response = await candidateService.updateCandidate(candidate.id, dataToSend);
        toast.success('Candidato actualizado exitosamente');
      } else {
        response = await candidateService.createCandidate(dataToSend);
        toast.success('Candidato creado exitosamente');
      }
      
      if (onSave) {
        onSave(response.data.candidato || response.data);
      }
      
      onClose();
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

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center p-4"
      onClick={handleBackdropClick}
    >
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h3 className="text-lg font-medium text-gray-900 flex items-center">
              <UserIcon className="h-5 w-5 mr-2 text-primary-600" />
              {isEditing ? 'Editar Candidato' : 'Nuevo Candidato'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {isEditing 
                ? 'Actualiza la información del candidato'
                : 'Completa la información básica del candidato'
              }
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 focus:outline-none focus:text-gray-600"
            disabled={saving}
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-6">
          <div className="space-y-4">
            {/* Nombre Completo */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nombre Completo <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <UserIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  className={`
                    block w-full pl-10 pr-3 py-2 border rounded-md shadow-sm placeholder-gray-400 
                    focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm
                    ${errors.nombre ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300'}
                  `}
                  placeholder="Ej: Juan Pérez García"
                  value={formData.nombre}
                  onChange={(e) => handleInputChange('nombre', e.target.value)}
                  disabled={saving}
                />
              </div>
              {errors.nombre && (
                <p className="text-sm text-red-600 mt-1">{errors.nombre}</p>
              )}
            </div>

            {/* Teléfono */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Teléfono <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <PhoneIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="tel"
                  className={`
                    block w-full pl-10 pr-3 py-2 border rounded-md shadow-sm placeholder-gray-400 
                    focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm
                    ${errors.telefono ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-gray-300'}
                  `}
                  placeholder="Ej: +52 55 1234 5678"
                  value={formData.telefono}
                  onChange={(e) => handleInputChange('telefono', e.target.value)}
                  disabled={saving}
                />
              </div>
              {errors.telefono && (
                <p className="text-sm text-red-600 mt-1">{errors.telefono}</p>
              )}
            </div>

            {/* Estado (solo para edición) */}
            {isEditing && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Estado
                </label>
                <select
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  value={formData.estado}
                  onChange={(e) => handleInputChange('estado', e.target.value)}
                  disabled={saving}
                >
                  {Object.entries(LABELS.CANDIDATE_STATES || {}).map(([key, label]) => (
                    <option key={key} value={key}>{label}</option>
                  ))}
                </select>
              </div>
            )}

            {/* Comentarios */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Comentarios y Observaciones
              </label>
              <div className="relative">
                <div className="absolute top-3 left-3 pointer-events-none">
                  <DocumentTextIcon className="h-5 w-5 text-gray-400" />
                </div>
                <textarea
                  rows={3}
                  className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Información adicional sobre el candidato, habilidades destacadas, experiencia relevante, etc."
                  value={formData.comentarios_finales}
                  onChange={(e) => handleInputChange('comentarios_finales', e.target.value)}
                  disabled={saving}
                />
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              disabled={saving}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {isEditing ? 'Actualizando...' : 'Creando...'}
                </>
              ) : (
                <>
                  <CheckCircleIcon className="h-4 w-4 mr-2" />
                  {isEditing ? 'Actualizar' : 'Crear Candidato'}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CandidateModal;