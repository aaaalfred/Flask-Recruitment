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
import useDebounce from '../hooks/useDebounce';

const Vacants = () => {
  const [vacants, setVacants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showCandidateManager, setShowCandidateManager] = useState(false);
  const [showVacantForm, setShowVacantForm] = useState(false);
  const [selectedVacant, setSelectedVacant] = useState(null);
  
  // Estados separados para inputs de búsqueda - OPTIMIZADO
  const [searchInput, setSearchInput] = useState('');
  const [clienteInput, setClienteInput] = useState('');
  const [filters, setFilters] = useState({
    estado: '',
    avance: ''
  });

  // Debouncing para búsquedas con 800ms delay para mejor UX
  const debouncedSearch = useDebounce(searchInput, 800);
  const debouncedCliente = useDebounce(clienteInput, 800);

  // Effect para cargar vacantes cuando cambien los filtros debounced
  useEffect(() => {
    fetchVacants();
  }, [currentPage, debouncedSearch, debouncedCliente, filters.estado, filters.avance]);

  const fetchVacants = async () => {
    try {
      setLoading(true);
      
      // Construir parámetros de búsqueda
      const searchParams = new URLSearchParams();
      if (currentPage > 1) searchParams.set('page', currentPage);
      searchParams.set('per_page', '10');
      if (filters.estado) searchParams.set('estado', filters.estado);
      if (debouncedSearch.trim()) searchParams.set('search', debouncedSearch.trim());
      if (debouncedCliente.trim()) searchParams.set('cliente', debouncedCliente.trim());
      if (filters.avance) searchParams.set('avance', filters.avance);

      const response = await vacantService.getVacants(
        currentPage, 
        10, 
        filters.estado || null,
        debouncedSearch.trim() || null,
        debouncedCliente.trim() || null,
        filters.avance || null
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

  const handleClearFilters = () => {
    setSearchInput('');
    setClienteInput('');
    setFilters({ estado: '', avance: '' });
    setCurrentPage(1);
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

  // Verificar si hay búsquedas activas pendientes
  const isSearching = (searchInput !== debouncedSearch) || (clienteInput !== debouncedCliente);

  if (loading && !isSearching) {
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

      {/* Filtros Optimizados */}
      <div className="bg-white rounded-lg shadow p-6">
        {/* Indicador de búsqueda activa */}
        {isSearching && (
          <div className="mb-4 bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              <span className="text-sm text-blue-700">Buscando...</span>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-5">
          {/* Búsqueda General */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar por nombre..."
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
            {/* Indicador individual */}
            {searchInput && searchInput !== debouncedSearch && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              </div>
            )}
          </div>

          {/* Cliente/CCP */}
          <div className="relative">
            <input
              type="text"
              placeholder="Cliente o CCP..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={clienteInput}
              onChange={(e) => setClienteInput(e.target.value)}
            />
            {/* Indicador individual */}
            {clienteInput && clienteInput !== debouncedCliente && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              </div>
            )}
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
              onClick={handleClearFilters}
              className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <FunnelIcon className="h-5 w-5 mr-2" />
              Limpiar
            </button>
          </div>
        </div>

        {/* Resumen de filtros activos */}
        {(debouncedSearch || debouncedCliente || filters.estado || filters.avance) && (
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">Filtros activos:</span>
            {debouncedSearch && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Nombre: "{debouncedSearch}"
              </span>
            )}
            {debouncedCliente && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Cliente: "{debouncedCliente}"
              </span>
            )}
            {filters.estado && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                Estado: {filters.estado}
              </span>
            )}
            {filters.avance && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                Avance: {filters.avance}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Tabla de vacantes */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {/* Loading overlay para búsquedas */}
        <div className="relative">
          {loading && (
            <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-10">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span className="text-sm text-gray-600">Cargando vacantes...</span>
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cliente / Vacante
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
                        {/* Información del Cliente */}
                        {vacant.cliente_nombre && (
                          <div className="flex items-center text-xs text-blue-600 mb-1">
                            <svg className="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1z" clipRule="evenodd" />
                            </svg>
                            <span className="font-medium">{vacant.cliente_nombre}</span>
                            <span className="ml-2 font-mono bg-blue-100 px-1 rounded text-xs">
                              {vacant.cliente_ccp}
                            </span>
                          </div>
                        )}
                        
                        {/* Nombre de la vacante */}
                        <div className="text-sm font-medium text-gray-900 flex items-center">
                          {getPriorityIcon(vacant.dias_transcurridos)} {vacant.nombre}
                        </div>
                        
                        {/* Información adicional */}
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
                  {(debouncedSearch || debouncedCliente) && (
                    <span className="text-blue-600"> (filtrado)</span>
                  )}
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
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {(debouncedSearch || debouncedCliente) ? 'No se encontraron vacantes' : 'No hay vacantes'}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {(debouncedSearch || debouncedCliente) 
              ? 'Intenta con otros términos de búsqueda.' 
              : 'Comienza creando tu primera vacante para el proceso de reclutamiento.'
            }
          </p>
          <div className="mt-6">
            {(debouncedSearch || debouncedCliente) ? (
              <button
                onClick={handleClearFilters}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FunnelIcon className="h-5 w-5 mr-2" />
                Limpiar Filtros
              </button>
            ) : (
              <button
                onClick={handleNewVacant}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Nueva Vacante
              </button>
            )}
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
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
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
        </div>
      )}
    </div>
  );
};

export default Vacants;