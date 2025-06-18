import React, { useState, useEffect } from 'react';
import { 
  PlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';
import { clientService } from '../services/api';
import { formatDate } from '../utils/helpers';
import toast from 'react-hot-toast';
import useDebounce from '../hooks/useDebounce';
import ClientForm from '../components/ClientForm';

const Clients = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showClientForm, setShowClientForm] = useState(false);
  const [selectedClient, setSelectedClient] = useState(null);
  const [showClientDetail, setShowClientDetail] = useState(false);
  
  // Estados para búsqueda optimizada
  const [searchInput, setSearchInput] = useState('');

  // Debouncing para búsqueda
  const debouncedSearch = useDebounce(searchInput, 800);

  useEffect(() => {
    fetchClients();
  }, [currentPage, debouncedSearch]);

  const fetchClients = async () => {
    try {
      setLoading(true);
      const response = await clientService.getClients(
        currentPage,
        10,
        debouncedSearch.trim() || null
      );
      setClients(response.data.clientes);
      setTotalPages(response.data.pages);
    } catch (error) {
      toast.error('Error al cargar los clientes');
      console.error('Error fetching clients:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewClient = () => {
    setSelectedClient(null);
    setShowClientForm(true);
  };

  const handleEditClient = (client) => {
    setSelectedClient(client);
    setShowClientForm(true);
  };

  const handleViewClient = async (client) => {
    try {
      const response = await clientService.getClient(client.id);
      setSelectedClient(response.data);
      setShowClientDetail(true);
    } catch (error) {
      toast.error('Error al cargar detalles del cliente');
    }
  };

  const handleClientSaved = () => {
    setShowClientForm(false);
    setSelectedClient(null);
    fetchClients();
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que deseas desactivar este cliente?')) {
      try {
        await clientService.deleteClient(id);
        toast.success('Cliente desactivado exitosamente');
        fetchClients();
      } catch (error) {
        toast.error('Error al desactivar el cliente');
      }
    }
  };

  const handleClearSearch = () => {
    setSearchInput('');
    setCurrentPage(1);
  };

  // Verificar si hay búsqueda activa pendiente
  const isSearching = searchInput !== debouncedSearch;

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
          <h1 className="text-2xl font-bold text-gray-900">🏢 Gestión de Clientes</h1>
          <p className="mt-2 text-sm text-gray-700">
            Administra los clientes y sus proyectos (CCP - Clave-Cliente-Proyecto)
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={handleNewClient}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Nuevo Cliente
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow p-6">
        {/* Indicador de búsqueda activa */}
        {isSearching && (
          <div className="mb-4 bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              <span className="text-sm text-blue-700">Buscando clientes...</span>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {/* Búsqueda */}
          <div className="relative col-span-2">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar por nombre o CCP..."
              className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
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

          {/* Limpiar filtros */}
          <div className="flex justify-end">
            <button 
              onClick={handleClearSearch}
              className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <FunnelIcon className="h-5 w-5 mr-2" />
              Limpiar
            </button>
          </div>
        </div>

        {/* Resumen de filtros activos */}
        {debouncedSearch && (
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="text-sm text-gray-500">Filtros activos:</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Búsqueda: "{debouncedSearch}"
            </span>
          </div>
        )}
      </div>

      {/* Tabla de clientes */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="relative">
          {/* Loading overlay */}
          {loading && (
            <div className="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center z-10">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                <span className="text-sm text-gray-600">Cargando clientes...</span>
              </div>
            </div>
          )}

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cliente
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    CCP
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vacantes
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha Creación
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {clients.map((client) => (
                  <tr key={client.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                            <BuildingOfficeIcon className="h-6 w-6 text-blue-600" />
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">
                            {client.nombre}
                          </div>
                          <div className="text-sm text-gray-500">
                            {client.activo ? 'Activo' : 'Inactivo'}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 font-mono">
                        {client.ccp}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {client.total_vacantes || 0} vacantes
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(client.fecha_creacion)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => handleViewClient(client)}
                          className="text-blue-600 hover:text-blue-900 p-1 rounded"
                          title="Ver detalles"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleEditClient(client)}
                          className="text-yellow-600 hover:text-yellow-900 p-1 rounded"
                          title="Editar"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(client.id)}
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
                  {debouncedSearch && (
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
      {!loading && clients.length === 0 && (
        <div className="text-center py-12">
          <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {debouncedSearch ? 'No se encontraron clientes' : 'No hay clientes'}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {debouncedSearch 
              ? 'Intenta con otros términos de búsqueda.' 
              : 'Comienza creando tu primer cliente.'
            }
          </p>
          <div className="mt-6">
            {debouncedSearch ? (
              <button
                onClick={handleClearSearch}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <FunnelIcon className="h-5 w-5 mr-2" />
                Limpiar Filtros
              </button>
            ) : (
              <button
                onClick={handleNewClient}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                Nuevo Cliente
              </button>
            )}
          </div>
        </div>
      )}

      {/* Modal de formulario de cliente */}
      {showClientForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <ClientForm
              client={selectedClient}
              onSave={handleClientSaved}
              onCancel={() => {
                setShowClientForm(false);
                setSelectedClient(null);
              }}
            />
          </div>
        </div>
      )}

      {/* Modal de detalle de cliente */}
      {showClientDetail && selectedClient && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-medium text-gray-900">
                  Detalles del Cliente
                </h3>
                <button
                  onClick={() => setShowClientDetail(false)}
                  className="text-gray-400 hover:text-gray-500"
                >
                  <span className="sr-only">Cerrar</span>
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="px-6 py-4">
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-900">Información General</h4>
                  <dl className="mt-2 grid grid-cols-1 gap-x-4 gap-y-2 sm:grid-cols-2">
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Nombre</dt>
                      <dd className="text-sm text-gray-900">{selectedClient.nombre}</dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">CCP</dt>
                      <dd className="text-sm text-gray-900 font-mono">{selectedClient.ccp}</dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Estado</dt>
                      <dd className="text-sm text-gray-900">
                        <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                          selectedClient.activo 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {selectedClient.activo ? 'Activo' : 'Inactivo'}
                        </span>
                      </dd>
                    </div>
                    <div>
                      <dt className="text-sm font-medium text-gray-500">Total Vacantes</dt>
                      <dd className="text-sm text-gray-900">{selectedClient.total_vacantes || 0}</dd>
                    </div>
                  </dl>
                </div>

                {/* Vacantes del cliente */}
                {selectedClient.vacantes_detalle && selectedClient.vacantes_detalle.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Vacantes Asociadas</h4>
                    <div className="space-y-2">
                      {selectedClient.vacantes_detalle.map((vacante) => (
                        <div key={vacante.id} className="border border-gray-200 rounded-md p-3">
                          <div className="flex items-center justify-between">
                            <h5 className="text-sm font-medium text-gray-900">{vacante.nombre}</h5>
                            <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${
                              vacante.estado === 'abierta' ? 'bg-blue-100 text-blue-800' :
                              vacante.estado === 'cerrada' ? 'bg-green-100 text-green-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {vacante.estado}
                            </span>
                          </div>
                          <div className="mt-1 text-xs text-gray-500">
                            Ejecutivo: {vacante.ejecutivo} • {vacante.total_candidatos} candidatos
                          </div>
                          <div className="mt-1 text-xs text-gray-400">
                            Creada: {formatDate(vacante.fecha_creacion)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
            
            <div className="px-6 py-4 border-t border-gray-200 bg-gray-50 flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowClientDetail(false);
                  handleEditClient(selectedClient);
                }}
                className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
              >
                <PencilIcon className="h-4 w-4 mr-2" />
                Editar
              </button>
              <button
                onClick={() => setShowClientDetail(false)}
                className="inline-flex items-center px-3 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Clients;