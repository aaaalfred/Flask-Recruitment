import React, { useState, useEffect } from 'react';
import { clientService } from '../services/api';
import toast from 'react-hot-toast';

const ClientForm = ({ client, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    ccp: ''
  });
  const [loading, setLoading] = useState(false);
  const [validatingCcp, setValidatingCcp] = useState(false);
  const [ccpValid, setCcpValid] = useState(null);

  useEffect(() => {
    if (client) {
      setFormData({
        nombre: client.nombre || '',
        ccp: client.ccp || ''
      });
    }
  }, [client]);

  const validateCcp = async (ccp) => {
    if (!ccp.trim()) {
      setCcpValid(null);
      return;
    }

    try {
      setValidatingCcp(true);
      const response = await clientService.validateCcp(ccp, client?.id);
      setCcpValid(response.data.valid);
    } catch (error) {
      setCcpValid(false);
    } finally {
      setValidatingCcp(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'ccp') {
      // Convertir a mayúsculas automáticamente
      const upperValue = value.toUpperCase();
      setFormData(prev => ({ ...prev, [name]: upperValue }));
      
      // Validar CCP después de un pequeño delay
      const timeoutId = setTimeout(() => {
        validateCcp(upperValue);
      }, 500);
      
      return () => clearTimeout(timeoutId);
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.nombre.trim() || !formData.ccp.trim()) {
      toast.error('Todos los campos son requeridos');
      return;
    }

    if (ccpValid === false) {
      toast.error('El CCP ingresado ya está en uso');
      return;
    }

    try {
      setLoading(true);
      
      if (client) {
        await clientService.updateClient(client.id, formData);
        toast.success('Cliente actualizado exitosamente');
      } else {
        await clientService.createClient(formData);
        toast.success('Cliente creado exitosamente');
      }
      
      onSave();
    } catch (error) {
      const message = error.response?.data?.message || 'Error al guardar el cliente';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-4">
        <h3 className="text-lg font-medium text-gray-900">
          {client ? 'Editar Cliente' : 'Nuevo Cliente'}
        </h3>
        <p className="mt-1 text-sm text-gray-600">
          {client 
            ? 'Actualiza la información del cliente.'
            : 'Agrega un nuevo cliente con su CCP (Clave-Cliente-Proyecto) único.'
          }
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Nombre del Cliente */}
        <div>
          <label htmlFor="nombre" className="block text-sm font-medium text-gray-700">
            Nombre del Cliente *
          </label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej: Grupo Empresarial ABC S.A. de C.V."
            value={formData.nombre}
            onChange={handleChange}
          />
        </div>

        {/* CCP */}
        <div>
          <label htmlFor="ccp" className="block text-sm font-medium text-gray-700">
            CCP (Clave-Cliente-Proyecto) *
          </label>
          <div className="relative">
            <input
              type="text"
              id="ccp"
              name="ccp"
              required
              className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none font-mono ${
                ccpValid === true 
                  ? 'border-green-300 focus:ring-green-500 focus:border-green-500' 
                  : ccpValid === false 
                  ? 'border-red-300 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500'
              }`}
              placeholder="Ej: ABC-001, XYZ-PROYECTO-2024"
              value={formData.ccp}
              onChange={handleChange}
            />
            
            {/* Indicador de validación */}
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              {validatingCcp && (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              )}
              {!validatingCcp && ccpValid === true && (
                <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              )}
              {!validatingCcp && ccpValid === false && (
                <svg className="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
            </div>
          </div>
          
          {/* Mensajes de validación */}
          {ccpValid === true && (
            <p className="mt-1 text-sm text-green-600">
              ✅ CCP disponible
            </p>
          )}
          {ccpValid === false && (
            <p className="mt-1 text-sm text-red-600">
              ❌ Este CCP ya está en uso por otro cliente
            </p>
          )}
          
          <p className="mt-1 text-xs text-gray-500">
            La CCP debe ser única y se convertirá automáticamente a mayúsculas.
          </p>
        </div>

        {/* Botones de acción */}
        <div className="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={loading || validatingCcp || ccpValid === false}
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Guardando...
              </div>
            ) : (
              client ? 'Actualizar Cliente' : 'Crear Cliente'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClientForm;