import React, { useState, useEffect, useRef } from 'react';
import { 
  ChevronDownIcon,
  MagnifyingGlassIcon,
  PlusIcon,
  BuildingOfficeIcon,
  CheckIcon
} from '@heroicons/react/24/outline';
import { clientService } from '../services/api';
import toast from 'react-hot-toast';
import ClientForm from './ClientForm';

const ClientSelector = ({ 
  selectedClient, 
  onClientSelect, 
  placeholder = "Seleccionar cliente...",
  disabled = false,
  required = false 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [showNewClientForm, setShowNewClientForm] = useState(false);
  
  const dropdownRef = useRef(null);
  const searchInputRef = useRef(null);

  // Cargar clientes activos al abrir el dropdown
  useEffect(() => {
    if (isOpen && clients.length === 0) {
      loadClients();
    }
  }, [isOpen]);

  // Buscar clientes cuando cambie el término de búsqueda
  useEffect(() => {
    if (isOpen && searchTerm.length > 0) {
      searchClients();
    } else if (isOpen && searchTerm.length === 0) {
      loadClients();
    }
  }, [searchTerm, isOpen]);

  // Cerrar dropdown al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Focus en el input de búsqueda al abrir
  useEffect(() => {
    if (isOpen && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [isOpen]);

  const loadClients = async () => {
    try {
      setLoading(true);
      const response = await clientService.getActiveClients();
      setClients(response.data.clientes || []);
    } catch (error) {
      console.error('Error loading clients:', error);
      toast.error('Error al cargar los clientes');
    } finally {
      setLoading(false);
    }
  };

  const searchClients = async () => {
    if (!searchTerm.trim()) {
      loadClients();
      return;
    }

    try {
      setLoading(true);
      const response = await clientService.searchClients(searchTerm);
      setClients(response.data.clientes || []);
    } catch (error) {
      console.error('Error searching clients:', error);
      toast.error('Error al buscar clientes');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectClient = (client) => {
    onClientSelect(client);
    setIsOpen(false);
    setSearchTerm('');
  };

  const handleNewClient = () => {
    setShowNewClientForm(true);
    setIsOpen(false);
  };

  const handleClientCreated = (newClient) => {
    setShowNewClientForm(false);
    onClientSelect(newClient);
    // Recargar lista de clientes
    loadClients();
    toast.success('Cliente creado y seleccionado exitosamente');
  };

  const filteredClients = searchTerm 
    ? clients.filter(client => 
        client.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.ccp.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : clients;

  return (
    <>
      <div className="relative" ref={dropdownRef}>
        {/* Botón principal */}
        <button
          type="button"
          className={`relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm ${
            disabled ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : ''
          } ${
            required && !selectedClient ? 'border-red-300' : ''
          }`}
          onClick={() => !disabled && setIsOpen(!isOpen)}
          disabled={disabled}
        >
          <span className="flex items-center">
            {selectedClient ? (
              <>
                <BuildingOfficeIcon className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0" />
                <span className="block truncate">
                  {selectedClient.nombre}
                  <span className="ml-2 text-xs text-gray-500 font-mono">
                    ({selectedClient.ccp})
                  </span>
                </span>
              </>
            ) : (
              <span className="block truncate text-gray-500">{placeholder}</span>
            )}
          </span>
          
          {!disabled && (
            <span className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
              <ChevronDownIcon 
                className={`h-5 w-5 text-gray-400 transition-transform duration-200 ${
                  isOpen ? 'transform rotate-180' : ''
                }`}
              />
            </span>
          )}
        </button>

        {/* Dropdown */}
        {isOpen && (
          <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
            {/* Búsqueda */}
            <div className="sticky top-0 z-10 bg-white border-b border-gray-200 px-3 py-2">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon className="h-4 w-4 text-gray-400" />
                </div>
                <input
                  ref={searchInputRef}
                  type="text"
                  className="block w-full pl-9 pr-3 py-1.5 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  placeholder="Buscar cliente o CCP..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            {/* Opción para crear nuevo cliente */}
            <div className="sticky top-12 z-10 bg-white border-b border-gray-200">
              <button
                type="button"
                onClick={handleNewClient}
                className="w-full text-left px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 flex items-center"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Crear nuevo cliente
              </button>
            </div>

            {/* Loading */}
            {loading && (
              <div className="px-3 py-2 text-sm text-gray-500 flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                Buscando...
              </div>
            )}

            {/* Lista de clientes */}
            {!loading && filteredClients.length > 0 && (
              <div className="max-h-40 overflow-y-auto">
                {filteredClients.map((client) => (
                  <button
                    key={client.id}
                    type="button"
                    className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-50 focus:bg-gray-50 focus:outline-none flex items-center justify-between ${
                      selectedClient?.id === client.id ? 'bg-blue-50' : ''
                    }`}
                    onClick={() => handleSelectClient(client)}
                  >
                    <div className="flex items-center flex-1 min-w-0">
                      <BuildingOfficeIcon className="h-4 w-4 text-gray-400 mr-2 flex-shrink-0" />
                      <div className="min-w-0 flex-1">
                        <div className="text-gray-900 truncate">{client.nombre}</div>
                        <div className="text-xs text-gray-500 font-mono">{client.ccp}</div>
                      </div>
                    </div>
                    {selectedClient?.id === client.id && (
                      <CheckIcon className="h-4 w-4 text-blue-600 flex-shrink-0" />
                    )}
                  </button>
                ))}
              </div>
            )}

            {/* Sin resultados */}
            {!loading && filteredClients.length === 0 && searchTerm && (
              <div className="px-3 py-2 text-sm text-gray-500">
                No se encontraron clientes con "{searchTerm}"
              </div>
            )}

            {/* Sin clientes */}
            {!loading && clients.length === 0 && !searchTerm && (
              <div className="px-3 py-2 text-sm text-gray-500">
                No hay clientes disponibles
              </div>
            )}
          </div>
        )}

        {/* Mensaje de validación */}
        {required && !selectedClient && (
          <p className="mt-1 text-sm text-red-600">
            Debes seleccionar un cliente
          </p>
        )}
      </div>

      {/* Modal para crear nuevo cliente */}
      {showNewClientForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <ClientForm
              client={null}
              onSave={handleClientCreated}
              onCancel={() => setShowNewClientForm(false)}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default ClientSelector;