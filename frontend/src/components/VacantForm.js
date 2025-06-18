import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { userService, vacantService } from '../services/api';
import toast from 'react-hot-toast';
import ClientSelector from './ClientSelector';

const VacantForm = ({ vacant = null, onSave, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm({
    defaultValues: {
      nombre: '',
      descripcion: '',
      cliente_id: '',
      reclutador_id: '',
      reclutador_lider_id: '', // Se configurará automáticamente
      candidatos_requeridos: 3,
      entrevistas_op: 3,
      vacantes: 1,
      avance: 'Creada', // Por defecto siempre "Creada"
      prioridad: 'media',
      envio_candidatos_rh: '',
      fecha_limite: '',
      comentarios: ''
    }
  });

  useEffect(() => {
    loadUsers();
    if (vacant) {
      // Poblar formulario con datos existentes
      Object.keys(vacant).forEach(key => {
        if ((key === 'fecha_limite' || key === 'envio_candidatos_rh') && vacant[key]) {
          // Convertir fecha para input datetime-local
          const date = new Date(vacant[key]);
          setValue(key, date.toISOString().slice(0, 16));
        } else {
          setValue(key, vacant[key]);
        }
      });
      
      // Establecer el cliente seleccionado si existe
      if (vacant.cliente_id) {
        setSelectedClient({
          id: vacant.cliente_id,
          nombre: vacant.cliente_nombre,
          ccp: vacant.cliente_ccp
        });
        setValue('cliente_id', vacant.cliente_id);
      }
    } else {
      // Para nuevas vacantes, configurar valores por defecto
      setValue('avance', 'Creada');
      // Buscar y asignar Fernanda Moreno como reclutador líder
      setFernandaAsLeader();
    }
  }, [vacant, setValue, users]);

  const setFernandaAsLeader = () => {
    // Buscar Fernanda Moreno en la lista de usuarios
    const fernanda = users.find(user => 
      user.nombre === 'Fernanda Moreno' && user.rol === 'reclutador_lider'
    );
    
    if (fernanda) {
      setValue('reclutador_lider_id', fernanda.id);
      console.log('Fernanda Moreno asignada como reclutador líder:', fernanda.id);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await userService.getUsers(1, 50);
      setUsers(response.data.usuarios || []);
    } catch (error) {
      console.error('Error loading users:', error);
      toast.error('Error cargando usuarios');
    }
  };

  // Funciones de validación
  const getTodayDateTime = () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    return now.toISOString().slice(0, 16);
  };

  const validateFutureDate = (value) => {
    if (!value) return true; // Campo opcional
    
    const selectedDate = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Inicio del día actual
    
    if (selectedDate <= today) {
      return 'La fecha debe ser posterior al día de hoy';
    }
    return true;
  };

  const validateFechaLimite = (value) => {
    if (!value) return true; // Campo opcional
    
    // Primero validar que sea fecha futura
    const futureValidation = validateFutureDate(value);
    if (futureValidation !== true) {
      return futureValidation;
    }
    
    // Luego validar que sea posterior a la fecha de envío
    const envioDate = watch('envio_candidatos_rh');
    if (envioDate) {
      const fechaEnvio = new Date(envioDate);
      const fechaLimite = new Date(value);
      
      if (fechaLimite <= fechaEnvio) {
        return 'La fecha límite debe ser posterior a la fecha de envío de candidatos';
      }
    }
    
    return true;
  };

  // Observar cambios en la fecha de envío para revalidar fecha límite
  const envioDate = watch('envio_candidatos_rh');
  
  // Efecto para revalidar fecha límite cuando cambie la fecha de envío
  useEffect(() => {
    if (envioDate) {
      // Trigger revalidation of fecha_limite
      const currentFechaLimite = watch('fecha_limite');
      if (currentFechaLimite) {
        setValue('fecha_limite', currentFechaLimite, { shouldValidate: true });
      }
    }
  }, [envioDate, setValue, watch]);

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      
      // Validar que se haya seleccionado un cliente
      if (!selectedClient) {
        toast.error('Debes seleccionar un cliente');
        setLoading(false);
        return;
      }
      
      // Convertir fechas si existen
      if (data.fecha_limite) {
        data.fecha_limite = new Date(data.fecha_limite).toISOString();
      }
      if (data.envio_candidatos_rh) {
        data.envio_candidatos_rh = new Date(data.envio_candidatos_rh).toISOString();
      }
      
      // Convertir números
      data.candidatos_requeridos = parseInt(data.candidatos_requeridos);
      data.entrevistas_op = parseInt(data.entrevistas_op);
      data.vacantes = parseInt(data.vacantes);
      
      // Asegurar que el cliente_id esté incluido
      if (selectedClient) {
        data.cliente_id = selectedClient.id;
      }

      let response;
      if (vacant) {
        response = await vacantService.updateVacant(vacant.id, data);
        toast.success('Vacante actualizada exitosamente');
      } else {
        response = await vacantService.createVacant(data);
        toast.success('Vacante creada exitosamente');
      }

      onSave(response.data.vacante);
    } catch (error) {
      const message = error.response?.data?.message || 'Error guardando vacante';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const reclutadores = users.filter(user => 
    user.rol === 'reclutador' || user.rol === 'reclutador_lider'
  );
  
  const reclutadoresLider = users.filter(user => user.rol === 'reclutador_lider');

  const handleClientSelect = (client) => {
    setSelectedClient(client);
    setValue('cliente_id', client?.id || '');
  };

  return (
    <div className="bg-white rounded-lg p-6">
      <div className="sticky top-0 bg-white z-10 pb-4 border-b border-gray-200 mb-6">
        <h2 className="text-xl font-semibold">
          {vacant ? 'Editar Vacante' : 'Nueva Vacante'}
        </h2>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Cliente */}
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-purple-900 mb-4">
            🏢 Información del Cliente
          </h3>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cliente y CCP *
            </label>
            <ClientSelector
              selectedClient={selectedClient}
              onClientSelect={handleClientSelect}
              placeholder="Seleccionar cliente y CCP..."
              required={true}
            />
            <p className="text-xs text-gray-500 mt-1">
              Selecciona el cliente y su Clave-Cliente-Proyecto (CCP) asociada
            </p>
            {!selectedClient && (
              <p className="text-red-500 text-sm mt-1">Debes seleccionar un cliente</p>
            )}
          </div>
        </div>

        {/* Información básica */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Nombre de la Posición *
          </label>
          <input
            type="text"
            {...register('nombre', { required: 'El nombre es requerido' })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ej: 2210 ACC FELIX CUEVAS"
          />
          {errors.nombre && (
            <p className="text-red-500 text-sm mt-1">{errors.nombre.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Descripción
          </label>
          <textarea
            {...register('descripcion')}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Descripción detallada de la posición..."
          />
        </div>

        {/* Configuración del proceso */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-blue-900 mb-4">
            🎯 Configuración del Proceso de Reclutamiento
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Vacantes Disponibles *
              </label>
              <input
                type="number"
                min="1"
                {...register('vacantes', { required: 'Número de vacantes requerido' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.vacantes && (
                <p className="text-red-500 text-sm mt-1">{errors.vacantes.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Candidatos Requeridos *
              </label>
              <input
                type="number"
                min="1"
                {...register('candidatos_requeridos', { required: 'Candidatos requeridos es obligatorio' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">Candidatos a presentar al ejecutivo</p>
              {errors.candidatos_requeridos && (
                <p className="text-red-500 text-sm mt-1">{errors.candidatos_requeridos.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Entrevistas Operativas
              </label>
              <input
                type="number"
                min="1"
                {...register('entrevistas_op')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">Número de entrevistas en el proceso</p>
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estado del Avance
            </label>
            <div className="w-full px-3 py-2 border border-gray-200 rounded-md bg-gray-50 text-gray-600">
              🆕 Creada (Por defecto para nuevas vacantes)
            </div>
            <p className="text-xs text-gray-500 mt-1">El estado se actualizará automáticamente durante el proceso</p>
            {/* Campo oculto para enviar el valor */}
            <input type="hidden" {...register('avance')} value="Creada" />
          </div>
        </div>

        {/* Asignación de personal */}
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-green-900 mb-4">
            👥 Asignación de Personal
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reclutador Asignado *
              </label>
              <select
                {...register('reclutador_id', { required: 'Reclutador es requerido' })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccionar reclutador...</option>
                {reclutadores.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.nombre} ({user.rol})
                  </option>
                ))}
              </select>
              {errors.reclutador_id && (
                <p className="text-red-500 text-sm mt-1">{errors.reclutador_id.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reclutador Líder
              </label>
              <div className="w-full px-3 py-2 border border-gray-200 rounded-md bg-green-50 text-green-700">
                👑 Fernanda Moreno (Asignada automáticamente)
              </div>
              <p className="text-xs text-gray-500 mt-1">Reclutador líder por defecto del sistema</p>
              {/* Campo oculto para enviar el valor */}
              <input type="hidden" {...register('reclutador_lider_id')} />
            </div>
          </div>
        </div>

        {/* Fechas y prioridad */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            📋 Fechas y Configuración
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prioridad
              </label>
              <select
                {...register('prioridad')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
                <option value="critica">Crítica</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📥 Envío de Candidatos a RH
              </label>
              <input
                type="datetime-local"
                {...register('envio_candidatos_rh', {
                  validate: validateFutureDate
                })}
                min={getTodayDateTime()}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">Fecha cuando se envían candidatos (debe ser futura)</p>
              {errors.envio_candidatos_rh && (
                <p className="text-red-500 text-sm mt-1">{errors.envio_candidatos_rh.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🗓️ Fecha Límite
              </label>
              <input
                type="datetime-local"
                {...register('fecha_limite', {
                  validate: validateFechaLimite
                })}
                min={envioDate || getTodayDateTime()}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                {envioDate 
                  ? 'Debe ser posterior a la fecha de envío de candidatos' 
                  : 'Fecha límite del proceso (debe ser futura)'
                }
              </p>
              {errors.fecha_limite && (
                <p className="text-red-500 text-sm mt-1">{errors.fecha_limite.message}</p>
              )}
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Comentarios Adicionales
            </label>
            <textarea
              {...register('comentarios')}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Comentarios, requisitos especiales, instrucciones adicionales..."
            />
          </div>
        </div>

        {/* Botones de acción */}
        <div className="sticky bottom-0 bg-white border-t border-gray-200 pt-4 mt-8">
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? 'Guardando...' : vacant ? 'Actualizar Vacante' : 'Crear Vacante'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default VacantForm;
