import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  DocumentArrowUpIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline';
import { candidateService } from '../services/api';
import { formatDate, getInitials, getAvatarColor } from '../utils/helpers';
import { LABELS, STATUS_COLORS, CANDIDATE_STATES } from '../utils/constants';
import toast from 'react-hot-toast';

const Candidates = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    search: '',
    estado: ''
  });

  useEffect(() => {
    fetchCandidates();
  }, [currentPage, filters]);

  const fetchCandidates = async () => {
    try {
      setLoading(true);
      const response = await candidateService.getCandidates(
        currentPage,
        10,
        filters.search || null,
        filters.estado || null
      );
      setCandidates(response.data.candidatos);
      setTotalPages(response.data.pages);
    } catch (error) {
      toast.error('Error al cargar los candidatos');
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1);
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
          <h1 className="text-2xl font-bold text-gray-900">Gestión de Candidatos</h1>
          <p className="mt-2 text-sm text-gray-700">
            Administra la base de datos de candidatos y su información
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <Link
            to="/candidates/new"
            className="btn-primary inline-flex items-center"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Nuevo Candidato
          </Link>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {/* Search */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar candidatos..."
              className="input-field pl-10"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
          </div>

          {/* Estado Filter */}
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

          {/* Filter Button */}
          <div className="flex justify-end">
            <button className="btn-secondary inline-flex items-center">
              <FunnelIcon className="h-5 w-5 mr-2" />
              Más Filtros
            </button>
          </div>
        </div>
      </div>

      {/* Cards Grid for Mobile */}
      <div className="lg:hidden space-y-4">
        {candidates.map((candidate) => (
          <div key={candidate.id} className="card">
            <div className="flex items-start space-x-4">
              {/* Avatar */}
              <div className={`h-12 w-12 rounded-full ${getAvatarColor(candidate.nombre)} flex items-center justify-center text-white font-medium`}>
                {getInitials(candidate.nombre)}
              </div>
              
              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">{candidate.nombre}</h3>
                    <p className="text-sm text-gray-500">{candidate.email}</p>
                    <p className="text-sm text-gray-500">{candidate.telefono}</p>
                  </div>
                  <span className={`badge ${STATUS_COLORS.CANDIDATE_STATES[candidate.estado]}`}>
                    {LABELS.CANDIDATE_STATES[candidate.estado]}
                  </span>
                </div>
                
                <div className="mt-3 flex items-center space-x-4 text-sm text-gray-500">
                  <span>{candidate.experiencia_anos} años exp.</span>
                  <span>{candidate.ubicacion}</span>
                  <span>{formatDate(candidate.fecha_creacion)}</span>
                </div>
                
                {/* Actions */}
                <div className="mt-4 flex space-x-2">
                  <Link
                    to={`/candidates/${candidate.id}`}
                    className="btn-secondary text-xs"
                  >
                    Ver Detalles
                  </Link>
                  <Link
                    to={`/candidates/${candidate.id}/edit`}
                    className="btn-secondary text-xs"
                  >
                    Editar
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Table for Desktop */}
      <div className="hidden lg:block card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Candidato
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Contacto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Experiencia
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
                    <div className="flex items-center">
                      <div className={`h-10 w-10 rounded-full ${getAvatarColor(candidate.nombre)} flex items-center justify-center text-white text-sm font-medium mr-4`}>
                        {getInitials(candidate.nombre)}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {candidate.nombre}
                        </div>
                        <div className="text-sm text-gray-500">
                          {candidate.ubicacion}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{candidate.email}</div>
                    <div className="text-sm text-gray-500">{candidate.telefono}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {candidate.experiencia_anos} años
                    </div>
                    <div className="text-sm text-gray-500">
                      {LABELS.ENGLISH_LEVELS[candidate.nivel_ingles]}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`badge ${STATUS_COLORS.CANDIDATE_STATES[candidate.estado]}`}>
                      {LABELS.CANDIDATE_STATES[candidate.estado]}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {candidate.reclutador}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(candidate.fecha_creacion)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div className="flex items-center justify-end space-x-2">
                      <Link
                        to={`/candidates/${candidate.id}`}
                        className="text-primary-600 hover:text-primary-900 p-1 rounded"
                        title="Ver detalles"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </Link>
                      <Link
                        to={`/candidates/${candidate.id}/edit`}
                        className="text-yellow-600 hover:text-yellow-900 p-1 rounded"
                        title="Editar"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </Link>
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

      {/* Empty State */}
      {!loading && candidates.length === 0 && (
        <div className="text-center py-12">
          <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No hay candidatos</h3>
          <p className="mt-1 text-sm text-gray-500">
            Comienza registrando tu primer candidato.
          </p>
          <div className="mt-6">
            <Link
              to="/candidates/new"
              className="btn-primary inline-flex items-center"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Nuevo Candidato
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default Candidates;
