import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  DocumentArrowUpIcon,
  UserGroupIcon,
  ArrowDownTrayIcon,
  ChartBarIcon,
  CheckIcon,
  XMarkIcon,
  InformationCircleIcon,
  PhoneIcon,
  MapPinIcon,
  BriefcaseIcon,
  CalendarIcon,
  UserIcon,
  ChevronDownIcon,
  ChevronUpIcon
} from '@heroicons/react/24/outline';
import { candidateService } from '../services/api';
import { formatDate, getInitials, getAvatarColor, exportToCSV } from '../utils/helpers';
import { LABELS, STATUS_COLORS } from '../utils/constants';
import toast from 'react-hot-toast';
import useDebounce from '../hooks/useDebounce';
import CandidateModal from '../components/CandidateModal';

const Candidates = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCandidates, setTotalCandidates] = useState(0);
  
  // Estados para filtros y búsqueda
  const [searchInput, setSearchInput] = useState('');
  const [filters, setFilters] = useState({
    estado: '',
    reclutador_id: ''
  });

  // Estados para UI
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [selectedCandidates, setSelectedCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [showQuickView, setShowQuickView] = useState(false);
  const [showStats, setShowStats] = useState(false);

  // Estados para el modal
  const [showModal, setShowModal] = useState(false);
  const [editingCandidate, setEditingCandidate] = useState(null);

  // Debouncing para búsqueda
  const debouncedSearch = useDebounce(searchInput, 800);

  // Efecto para cargar candidatos
  useEffect(() => {
    fetchCandidates();
  }, [currentPage, debouncedSearch, filters]);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidateService.getCandidates(
        currentPage,
        10,
        debouncedSearch.trim() || null,
        filters.estado || null
      );
      setCandidates(response.data.candidatos);
      setTotalPages(response.data.pages);
      setTotalCandidates(response.data.total);
    } catch (error) {
      toast.error('Error al cargar los candidatos');
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  // Estadísticas calculadas
  const stats = useMemo(() => {
    return {
      total: totalCandidates,
      activos: candidates.filter(c => c.estado === 'activo').length,
      inactivos: candidates.filter(c => c.estado === 'inactivo').length,
      blacklist: candidates.filter(c => c.estado === 'blacklist').length
    };
  }, [candidates, totalCandidates]);

  // Manejadores de eventos
  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
  };

  const handleClearFilters = () => {
    setSearchInput('');
    setFilters({
      estado: '',
      reclutador_id: ''
    });
    setCurrentPage(1);
  };

  const handleSelectCandidate = (candidateId) => {
    setSelectedCandidates(prev => 
      prev.includes(candidateId)
        ? prev.filter(id => id !== candidateId)
        : [...prev, candidateId]
    );
  };

  const handleSelectAll = () => {
    setSelectedCandidates(
      selectedCandidates.length === candidates.length 
        ? [] 
        : candidates.map(c => c.id)
    );
  };

  const handleBulkAction = async (action) => {
    if (selectedCandidates.length === 0) {
      toast.error('Selecciona al menos un candidato');
      return;
    }

    if (!window.confirm(`¿Estás seguro de que deseas ${action} ${selectedCandidates.length} candidato(s)?`)) {
      return;
    }

    try {
      // Implementar acciones en lote aquí
      toast.success(`Acción "${action}" aplicada a ${selectedCandidates.length} candidatos`);
      setSelectedCandidates([]);
      fetchCandidates();
    } catch (error) {
      toast.error(`Error al ejecutar acción: ${error.message}`);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que deseas desactivar este candidato?')) {
      try {
        await candidateService.deleteCandidate(id);
        toast.success('Candidato desactivado exitosamente');
        fetchCandidates();
      } catch (error) {
        toast.error('Error al desactivar el candidato');
      }
    }
  };

  const handleQuickView = (candidate) => {
    setSelectedCandidate(candidate);
    setShowQuickView(true);
  };

  const handleExport = () => {
    const exportData = candidates.map(candidate => ({
      'Nombre': candidate.nombre,
      'Teléfono': candidate.telefono,
      'Estado': LABELS.CANDIDATE_STATES[candidate.estado],

      'Reclutador': candidate.reclutador,
      'Fecha de Creación': formatDate(candidate.fecha_creacion)
    }));

    exportToCSV(exportData, `candidatos_${new Date().toISOString().split('T')[0]}`);
    toast.success('Datos exportados exitosamente');
  };

  // Manejadores del modal
  const handleNewCandidate = () => {
    setEditingCandidate(null);
    setShowModal(true);
  };

  const handleEditCandidate = (candidate) => {
    setEditingCandidate(candidate);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCandidate(null);
  };

  const handleSaveCandidate = (savedCandidate) => {
    // Recargar la lista de candidatos
    fetchCandidates();
  };

  const isSearching = searchInput !== debouncedSearch;
  const hasActiveFilters = Object.values(filters).some(value => value !== '') || debouncedSearch;

  // Componente de estadísticas rápidas
  const StatsCard = ({ title, value, color, icon: Icon }) => (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="flex items-center">
        <div className={`flex-shrink-0 p-2 rounded-lg ${color}`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
        <div className="ml-3">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-lg font-semibold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );

  // Modal de vista rápida
  const QuickViewModal = () => {
    if (!showQuickView || !selectedCandidate) return null;

    return (
      <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
          <div className="mt-3">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-medium text-gray-900">Vista Rápida</h3>
              <button
                onClick={() => setShowQuickView(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className={`h-12 w-12 rounded-full ${getAvatarColor(selectedCandidate.nombre)} flex items-center justify-center text-white font-medium`}>
                  {getInitials(selectedCandidate.nombre)}
                </div>
                <div>
                  <h4 className="font-medium text-gray-900">{selectedCandidate.nombre}</h4>
                  <span className={`badge ${STATUS_COLORS.CANDIDATE_STATES[selectedCandidate.estado]}`}>
                    {LABELS.CANDIDATE_STATES[selectedCandidate.estado]}
                  </span>
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-center">
                  <PhoneIcon className="h-4 w-4 text-gray-400 mr-2" />
                  <span>{selectedCandidate.telefono}</span>
                </div>
                
                <div className="flex items-center">
                  <UserIcon className="h-4 w-4 text-gray-400 mr-2" />
                  <span>Reclutador: {selectedCandidate.reclutador}</span>
                </div>
              </div>

              <div className="flex space-x-2 pt-4">
                <Link
                  to={`/candidates/${selectedCandidate.id}`}
                  className="btn-primary flex-1 text-center"
                  onClick={() => setShowQuickView(false)}
                >
                  Ver Detalles
                </Link>
                <button
                  onClick={() => {
                    handleEditCandidate(selectedCandidate);
                    setShowQuickView(false);
                  }}
                  className="btn-secondary flex-1"
                >
                  Editar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Loading principal
  if (loading && !isSearching && candidates.length === 0) {
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
          <h1 className="text-2xl font-bold text-gray-900">👥 Gestión de Candidatos</h1>
          <p className="mt-2 text-sm text-gray-700">
            Administra la base de datos de candidatos y su información
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-3">
          <button
            onClick={() => setShowStats(!showStats)}
            className="btn-secondary inline-flex items-center"
          >
            <ChartBarIcon className="h-5 w-5 mr-2" />
            Estadísticas
          </button>
          <button
            onClick={handleExport}
            className="btn-secondary inline-flex items-center"
            disabled={candidates.length === 0}
          >
            <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
            Exportar
          </button>
          <button
            onClick={handleNewCandidate}
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Nuevo Candidato
          </button>
        </div>
      </div>

      {/* Estadísticas rápidas */}
      {showStats && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatsCard
            title="Total Candidatos"
            value={stats.total}
            color="bg-blue-500"
            icon={UserGroupIcon}
          />
          <StatsCard
            title="Candidatos Activos"
            value={stats.activos}
            color="bg-green-500"
            icon={CheckIcon}
          />
          <StatsCard
            title="Candidatos Inactivos"
            value={stats.inactivos}
            color="bg-yellow-500"
            icon={XMarkIcon}
          />
          <StatsCard
            title="En Lista Negra"
            value={stats.blacklist}
            color="bg-red-500"
            icon={XMarkIcon}
          />
        </div>
      )}

      {/* Filtros */}
      <div className="card">
        {/* Indicador de búsqueda activa */}
        {isSearching && (
          <div className="mb-4 bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              <span className="text-sm text-blue-700">Buscando candidatos...</span>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
          {/* Búsqueda */}
          <div className="relative col-span-2">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar por nombre o teléfono..."
              className="input-field pl-10 pr-10"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
            {searchInput && searchInput !== debouncedSearch && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              </div>
            )}
          </div>

          {/* Estado */}
          <div className="relative">
            <select
              className="input-field"
              value={filters.estado}
              onChange={(e) => handleFilterChange('estado', e.target.value)}
            >
              <option value="">Todos los estados</option>
              {Object.entries(LABELS.CANDIDATE_STATES).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          {/* Botones de acción */}
          <div className="flex justify-end space-x-2">
            <button
              onClick={handleClearFilters}
              className="btn-secondary"
              disabled={!hasActiveFilters}
            >
              Limpiar
            </button>
          </div>
        </div>

        {/* Resumen de filtros activos */}
        {hasActiveFilters && (
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">Filtros activos:</span>
            {debouncedSearch && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Búsqueda: "{debouncedSearch}"
              </span>
            )}
            {filters.estado && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Estado: {LABELS.CANDIDATE_STATES[filters.estado]}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Acciones en lote */}
      {selectedCandidates.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="text-sm font-medium text-blue-900">
                {selectedCandidates.length} candidato(s) seleccionado(s)
              </span>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleBulkAction('activar')}
                className="text-sm bg-green-600 text-white px-3 py-1 rounded-md hover:bg-green-700"
              >
                Activar
              </button>
              <button
                onClick={() => handleBulkAction('desactivar')}
                className="text-sm bg-red-600 text-white px-3 py-1 rounded-md hover:bg-red-700"
              >
                Desactivar
              </button>
              <button
                onClick={() => setSelectedCandidates([])}
                className="text-sm bg-gray-600 text-white px-3 py-1 rounded-md hover:bg-gray-700"
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Vista de tabla */}
      <div className="card overflow-hidden">
        <div className="relative">
          {loading && (
            <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-10">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span className="text-sm text-gray-600">Cargando candidatos...</span>
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left">
                    <input
                      type="checkbox"
                      className="rounded border-gray-300"
                      checked={selectedCandidates.length === candidates.length && candidates.length > 0}
                      onChange={handleSelectAll}
                    />
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Candidato
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contacto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Reclutador
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {candidates.map((candidate) => (
                  <tr key={candidate.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="checkbox"
                        className="rounded border-gray-300"
                        checked={selectedCandidates.includes(candidate.id)}
                        onChange={() => handleSelectCandidate(candidate.id)}
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`h-10 w-10 rounded-full ${getAvatarColor(candidate.nombre)} flex items-center justify-center text-white text-sm font-medium mr-4`}>
                          {getInitials(candidate.nombre)}
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-900">
                            {candidate.nombre}
                          </div>

                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        <PhoneIcon className="h-4 w-4 inline mr-1" />
                        {candidate.telefono}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`badge ${STATUS_COLORS.CANDIDATE_STATES[candidate.estado]}`}>
                        {LABELS.CANDIDATE_STATES[candidate.estado]}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <UserIcon className="h-4 w-4 inline mr-1" />
                      {candidate.reclutador}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <CalendarIcon className="h-4 w-4 inline mr-1" />
                      {formatDate(candidate.fecha_creacion)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => handleQuickView(candidate)}
                          className="text-blue-600 hover:text-blue-900 p-1 rounded"
                          title="Vista rápida"
                        >
                          <InformationCircleIcon className="h-4 w-4" />
                        </button>
                        <Link
                          to={`/candidates/${candidate.id}`}
                          className="text-primary-600 hover:text-primary-900 p-1 rounded"
                          title="Ver detalles"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </Link>
                        <button
                          onClick={() => handleEditCandidate(candidate)}
                          className="text-yellow-600 hover:text-yellow-900 p-1 rounded"
                          title="Editar"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </button>
                        <button
                          className="text-green-600 hover:text-green-900 p-1 rounded"
                          title="Subir documento"
                        >
                          <DocumentArrowUpIcon className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(candidate.id)}
                          className="text-red-600 hover:text-red-900 p-1 rounded"
                          title="Desactivar"
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

        {/* Pagination */}
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
                  Mostrando {candidates.length} de {totalCandidates} candidatos
                  {hasActiveFilters && (
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

      {/* Empty State */}
      {!loading && candidates.length === 0 && (
        <div className="text-center py-12">
          <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {hasActiveFilters ? 'No se encontraron candidatos' : 'No hay candidatos'}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {hasActiveFilters 
              ? 'Intenta con otros términos de búsqueda.' 
              : 'Comienza registrando tu primer candidato.'
            }
          </p>
          <div className="mt-6">
            {hasActiveFilters ? (
              <button
                onClick={handleClearFilters}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FunnelIcon className="h-5 w-5 mr-2" />
                Limpiar Filtros
              </button>
            ) : (
              <button
                onClick={handleNewCandidate}
                className="btn-primary inline-flex items-center"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Nuevo Candidato
              </button>
            )}
          </div>
        </div>
      )}

      {/* Modal de vista rápida */}
      <QuickViewModal />

      {/* Modal de candidato */}
      <CandidateModal
        isOpen={showModal}
        onClose={handleCloseModal}
        candidate={editingCandidate}
        onSave={handleSaveCandidate}
      />
    </div>
  );
};

export default Candidates;