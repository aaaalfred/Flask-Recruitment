import React, { useState, useEffect } from 'react';
import { candidatePositionService } from '../services/api';
import toast from 'react-hot-toast';

const CandidateVacantManager = ({ vacanteId, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [showEvaluationModal, setShowEvaluationModal] = useState(false);

  useEffect(() => {
    if (vacanteId) {
      loadCandidatesByVacant();
    }
  }, [vacanteId]);

  const loadCandidatesByVacant = async () => {
    try {
      setLoading(true);
      const response = await candidatePositionService.getCandidatesByVacant(vacanteId);
      setData(response.data);
    } catch (error) {
      console.error('Error loading candidates:', error);
      toast.error('Error cargando candidatos');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluateCandidate = (candidato) => {
    setSelectedCandidate(candidato);
    setShowEvaluationModal(true);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'postulado':
        return 'bg-gray-100 text-gray-800';
      case 'en_proceso':
        return 'bg-yellow-100 text-yellow-800';
      case 'aceptado_supervisor':
        return 'bg-green-100 text-green-800';
      case 'rechazado_supervisor':
        return 'bg-red-100 text-red-800';
      case 'contratado':
        return 'bg-emerald-100 text-emerald-800';
      case 'rechazado':
        return 'bg-red-200 text-red-900';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getContratadoStatusColor = (status) => {
    switch (status) {
      case 'pendiente':
        return 'bg-blue-100 text-blue-800';
      case 'contratado':
        return 'bg-green-100 text-green-800';
      case 'rechazado':
        return 'bg-red-100 text-red-800';
      case 'no_contratable':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getContratadoStatusText = (status) => {
    switch (status) {
      case 'pendiente':
        return 'Pendiente';
      case 'contratado':
        return 'Contratado';
      case 'rechazado':
        return 'Rechazado';
      case 'no_contratable':
        return 'No Contratable';
      default:
        return 'Sin Estado';
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-center">Cargando candidatos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-semibold">
              Gestión de Candidatos - {data?.vacante?.nombre}
            </h2>
            <p className="text-blue-100 text-sm">
              {data?.estadisticas?.total_candidatos || 0} candidatos • 
              {data?.estadisticas?.contratados || 0} contratados
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-blue-100 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>

        {/* Estadísticas */}
        <div className="p-6 bg-gray-50 border-b">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {data?.estadisticas?.total_candidatos || 0}
              </div>
              <div className="text-sm text-gray-500">Total</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {data?.estadisticas?.aceptados_supervisor || 0}
              </div>
              <div className="text-sm text-gray-500">Aceptados</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">
                {data?.estadisticas?.contratados || 0}
              </div>
              <div className="text-sm text-gray-500">Contratados</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {data?.estadisticas?.rechazados || 0}
              </div>
              <div className="text-sm text-gray-500">Rechazados</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {data?.estadisticas?.pendientes || 0}
              </div>
              <div className="text-sm text-gray-500">Pendientes</div>
            </div>
          </div>
        </div>

        {/* Lista de candidatos */}
        <div className="flex-1 overflow-y-auto modal-scroll p-6" style={{ scrollbarWidth: 'thin' }}>
          {data?.candidatos?.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 text-6xl mb-4">👥</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No hay candidatos asignados
              </h3>
              <p className="text-gray-500">
                Esta vacante aún no tiene candidatos asignados.
              </p>
            </div>
          ) : (
            <div className="space-y-4 pb-4">
              {data?.candidatos?.map((item) => (
                <div key={item.asignacion_id} className="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-medium text-gray-900">
                          {item.candidato.nombre}
                        </h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(item.proceso.status)}`}>
                          {item.proceso.status || 'Sin estado'}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getContratadoStatusColor(item.proceso.contratado_status)}`}>
                          {getContratadoStatusText(item.proceso.contratado_status)}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                        <div>
                          <span className="font-medium">Email:</span> {item.candidato.email}
                        </div>
                        <div>
                          <span className="font-medium">Teléfono:</span> {item.candidato.telefono || 'No disponible'}
                        </div>
                        <div>
                          <span className="font-medium">Experiencia:</span> {item.candidato.experiencia_anos || 0} años
                        </div>
                      </div>

                      {item.proceso.archivo_cv && (
                        <div className="mt-2 text-sm text-gray-600">
                          <span className="font-medium">CV:</span> {item.proceso.archivo_cv}
                        </div>
                      )}

                      {item.proceso.aceptado && (
                        <div className="mt-2 flex items-center text-sm text-green-600">
                          <span className="mr-1">✅</span>
                          Aceptado por supervisor
                        </div>
                      )}

                      {!item.proceso.se_presento && (
                        <div className="mt-2 flex items-center text-sm text-red-600">
                          <span className="mr-1">❌</span>
                          No se presentó
                        </div>
                      )}

                      {item.proceso.comentarios_finales && (
                        <div className="mt-3 p-3 bg-gray-50 rounded">
                          <span className="font-medium text-gray-700">Comentarios:</span>
                          <p className="text-sm text-gray-600 mt-1">
                            {item.proceso.comentarios_finales}
                          </p>
                        </div>
                      )}

                      <div className="mt-2 text-xs text-gray-500">
                        Asignado: {new Date(item.proceso.fecha_asignacion).toLocaleDateString()}
                        {item.proceso.fecha_decision_final && (
                          <span className="ml-3">
                            Decisión final: {new Date(item.proceso.fecha_decision_final).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="ml-4 flex flex-col space-y-2">
                      <button
                        onClick={() => handleEvaluateCandidate(item)}
                        className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                      >
                        Evaluar
                      </button>
                      
                      {item.candidato.cv_url && (
                        <a
                          href={item.candidato.cv_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3 py-1 bg-gray-600 text-white text-sm rounded hover:bg-gray-700 text-center"
                        >
                          Ver CV
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 flex justify-end border-t">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Cerrar
          </button>
        </div>
      </div>

      {/* Modal de evaluación */}
      {showEvaluationModal && selectedCandidate && (
        <CandidateEvaluationModal
          candidate={selectedCandidate}
          onClose={() => {
            setShowEvaluationModal(false);
            setSelectedCandidate(null);
          }}
          onSave={() => {
            setShowEvaluationModal(false);
            setSelectedCandidate(null);
            loadCandidatesByVacant();
          }}
        />
      )}
    </div>
  );
};

// Componente para modal de evaluación
const CandidateEvaluationModal = ({ candidate, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    aceptado: candidate.proceso.aceptado || false,
    contratado_status: candidate.proceso.contratado_status || 'pendiente',
    comentarios_finales: candidate.proceso.comentarios_finales || '',
    se_presento: candidate.proceso.se_presento !== false,
    motivo_rechazo: candidate.proceso.motivo_rechazo || ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      await candidatePositionService.updateAssignment(candidate.asignacion_id, formData);
      toast.success('Evaluación guardada exitosamente');
      onSave();
    } catch (error) {
      const message = error.response?.data?.message || 'Error guardando evaluación';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-60 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div className="bg-blue-600 text-white px-6 py-4 rounded-t-lg">
          <h3 className="text-lg font-semibold">
            Evaluar Candidato
          </h3>
          <p className="text-blue-100 text-sm">
            {candidate.candidato.nombre}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.aceptado}
                onChange={(e) => setFormData({...formData, aceptado: e.target.checked})}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700">
                Aceptado por supervisor
              </span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estado de contratación
            </label>
            <select
              value={formData.contratado_status}
              onChange={(e) => setFormData({...formData, contratado_status: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="pendiente">Pendiente</option>
              <option value="contratado">Contratado</option>
              <option value="rechazado">Rechazado</option>
              <option value="no_contratable">No Contratable</option>
            </select>
          </div>

          <div>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.se_presento}
                onChange={(e) => setFormData({...formData, se_presento: e.target.checked})}
                className="rounded border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700">
                Se presentó a las citas/tienda
              </span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Comentarios finales
            </label>
            <textarea
              value={formData.comentarios_finales}
              onChange={(e) => setFormData({...formData, comentarios_finales: e.target.value})}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Explique la razón de la decisión..."
            />
          </div>

          {formData.contratado_status === 'rechazado' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Motivo de rechazo
              </label>
              <input
                type="text"
                value={formData.motivo_rechazo}
                onChange={(e) => setFormData({...formData, motivo_rechazo: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Motivo específico..."
              />
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Guardando...' : 'Guardar Evaluación'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CandidateVacantManager;
