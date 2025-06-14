import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  BriefcaseIcon,
  UserGroupIcon,
  CalendarDaysIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { vacantService } from '../services/api';
import { formatDate } from '../utils/helpers';
import toast from 'react-hot-toast';
import CandidateVacantManager from '../components/CandidateVacantManager';
import VacantForm from '../components/VacantForm';

const Vacants = () => {
  const [vacants, setVacants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showCandidateManager, setShowCandidateManager] = useState(false);
  const [showVacantForm, setShowVacantForm] = useState(false);
  const [selectedVacant, setSelectedVacant] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    estado: '',
    avance: ''
  });

  useEffect(() => {
    fetchVacants();
  }, [currentPage, filters]);

  const fetchVacants = async () => {
    try {
      setLoading(true);
      const response = await vacantService.getVacants(
        currentPage, 
        10, 
        filters.estado || null
      );
      setVacants(response.data.vacantes);
      setTotalPages(response.data.pages);
    } catch (error) {
      toast.error('Error al cargar las vacantes');
      console.error('Error fetching vacants:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que deseas cancelar esta vacante?')) {
      try {
        await vacantService.deleteVacant(id);
        toast.success('Vacante cancelada exitosamente');
        fetchVacants();
      } catch (error) {
        toast.error('Error al cancelar la vacante');
      }
    }
  };

  const handleManageCandidates = (vacant) => {
    setSelectedVacant(vacant);
    setShowCandidateManager(true);
  };

  const handleNewVacant = () => {
    setSelectedVacant(null);
    setShowVacantForm(true);
  };

  const handleEditVacant = (vacant) => {
    setSelectedVacant(vacant);
    setShowVacantForm(true);
  };

  const handleVacantSaved = () => {
    setShowVacantForm(false);
    setSelectedVacant(null);
    fetchVacants();
  };

  const getAvanceColor = (avance) => {
    switch (avance) {
      case 'Creada':
        return 'bg-gray-100 text-gray-800';
      case 'Buscando candidatos':
        return 'bg-yellow-100 text-yellow-800';
      case 'Candidatos enviados a RH':
        return 'bg-blue-100 text-blue-800';
      case 'En proceso de entrevistas':
        return 'bg-purple-100 text-purple-800';
      case 'Seleccionando candidatos':
        return 'bg-orange-100 text-orange-800';
      case 'Posiciones cubiertas':
        return 'bg-green-100 text-green-800';
      case 'Finalizada':
        return 'bg-green-200 text-green-900';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusFinalColor = (status) => {
    switch (status) {
      case 'abierta':
        return 'bg-blue-100 text-blue-800';
      case 'cubierta':
        return 'bg-green-100 text-green-800';
      case 'pausada':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelada':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityIcon = (dias) => {
    if (dias > 100) return '🔴';
    if (dias > 60) return '🟡';
    if (dias > 30) return '🟠';
    return '🟢';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">📋 Gestión de Vacantes</h1>
          <p className="mt-2 text-sm text-gray-700">
            Administra las posiciones y gestiona el proceso completo de reclutamiento
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={handleNewVacant}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Nueva Vacante
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
          {/* Búsqueda */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar vacantes..."
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>

          {/* Estado */}
          <div className="relative">
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filters.estado}
              onChange={(e) => handleFilterChange('estado', e.target.value)}
            >
              <option value="">Todos los estados</option>
              <option value="abierta">Abierta</option>
              <option value="pausada">Pausada</option>
              <option value="cerrada">Cerrada</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>

          {/* Avance */}
          <div className="relative">
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filters.avance}
              onChange={(e) => handleFilterChange('avance', e.target.value)}
            >
              <option value="">Todos los avances</option>
              <option value="Creada">Creada</option>
              <option value="Buscando candidatos">Buscando candidatos</option>
              <option value="Candidatos enviados a RH">Candidatos enviados a RH</option>
              <option value="En proceso de entrevistas">En proceso de entrevistas</option>
              <option value="Seleccionando candidatos">Seleccionando candidatos</option>
              <option value="Posiciones cubiertas">Posiciones cubiertas</option>
              <option value="Finalizada">Finalizada</option>
            </select>
          </div>

          {/* Limpiar filtros */}
          <div className="flex justify-end">
            <button 
              onClick={() => setFilters({ search: '', estado: '', avance: '' })}
              className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <FunnelIcon className="h-5 w-5 mr-2" />
              Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* Tabla de vacantes */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vacante / Ubicación
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Avance del Proceso
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Candidatos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tiempo / Prioridad
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Equipo
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {vacants.map((vacant) => (
                <tr key={vacant.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900 flex items-center">
                        {getPriorityIcon(vacant.dias_transcurridos)} {vacant.nombre}
                      </div>
                      <div className="text-sm text-gray-500">
                        📍 {vacant.ubicacion || 'Ubicación no especificada'}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        {vacant.vacantes} {vacant.vacantes === 1 ? 'posición' : 'posiciones'} • 
                        {vacant.candidatos_requeridos} candidatos requeridos
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="space-y-1">
                      <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getAvanceColor(vacant.avance)}`}>
                        {vacant.avance || 'Sin avance'}
                      </span>
                      <div>
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getStatusFinalColor(vacant.status_final)}`}>
                          {vacant.status_final || 'abierta'}
                        </span>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      <div className="flex items-center space-x-1">
                        <UserGroupIcon className="h-4 w-4 text-gray-400" />
                        <span>{vacant.total_candidatos || 0} Total</span>
                      </div>
                      <div className="text-xs text-gray-500 space-y-1 mt-1">
                        <div>✅ {vacant.candidatos_aceptados || 0} Aceptados</div>
                        <div>🎯 {vacant.candidatos_contratados || 0} Contratados</div>
                        <div>❌ {vacant.candidatos_rechazados || 0} Rechazados</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      <div className="flex items-center space-x-1">
                        <ClockIcon className="h-4 w-4 text-gray-400" />
                        <span>{vacant.dias_transcurridos || 0} días</span>
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        <CalendarDaysIcon className="h-3 w-3 inline mr-1" />
                        {formatDate(vacant.fecha_solicitud)}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      <div className="text-xs text-gray-500 space-y-1">
                        <div>👤 <strong>Ejecutivo:</strong> {vacant.ejecutivo}</div>
                        <div>🔍 <strong>Reclutador:</strong> {vacant.reclutador}</div>
                        {vacant.reclutador_lider && (
                          <div>👑 <strong>Líder:</strong> {vacant.reclutador_lider}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center justify-end space-x-2">
                      <button
                        onClick={() => handleManageCandidates(vacant)}
                        className="text-blue-600 hover:text-blue-900 p-1 rounded"
                        title="Gestionar candidatos"
                      >
                        <UserGroupIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleEditVacant(vacant)}
                        className="text-yellow-600 hover:text-yellow-900 p-1 rounded"
                        title="Editar vacante"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(vacant.id)}
                        className="text-red-600 hover:text-red-900 p-1 rounded"
                        title="Cancelar vacante"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Paginación */}
        {totalPages > 1 && (
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Siguiente
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Página <span className="font-medium">{currentPage}</span> de{' '}
                  <span className="font-medium">{totalPages}</span>
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Anterior
                  </button>
                  <button
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Siguiente
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Estado vacío */}
      {!loading && vacants.length === 0 && (
        <div className="text-center py-12">
          <BriefcaseIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay vacantes</h3>
          <p className="mt-1 text-sm text-gray-500">
            Comienza creando tu primera vacante para el proceso de reclutamiento.
          </p>
          <div className="mt-6">
            <button
              onClick={handleNewVacant}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Nueva Vacante
            </button>
          </div>
        </div>
      )}

      {/* Modal de gestión de candidatos */}
      {showCandidateManager && selectedVacant && (
        <CandidateVacantManager
          vacanteId={selectedVacant.id}
          onClose={() => {
            setShowCandidateManager(false);
            setSelectedVacant(null);
            fetchVacants(); // Refrescar datos
          }}
        />
      )}

      {/* Modal de formulario de vacante */}
      {showVacantForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
            <VacantForm
              vacant={selectedVacant}
              onSave={handleVacantSaved}
              onCancel={() => {
                setShowVacantForm(false);
                setSelectedVacant(null);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Vacants;
