import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { userService, vacantService } from '../services/api';
import toast from 'react-hot-toast';

const VacantForm = ({ vacant = null, onSave, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [users, setUsers] = useState([]);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue
  } = useForm({
    defaultValues: {
      nombre: '',
      descripcion: '',
      reclutador_id: '',
      reclutador_lider_id: '',
      candidatos_requeridos: 3,
      entrevistas_op: 3,
      vacantes: 1,
      avance: 'Creada',
      ubicacion: '',
      modalidad: 'presencial',
      prioridad: 'media',
      salario_min: '',
      salario_max: '',
      fecha_limite: '',
      comentarios: ''
    }
  });

  useEffect(() => {
    loadUsers();
    if (vacant) {
      // Poblar formulario con datos existentes
      Object.keys(vacant).forEach(key => {
        if (key === 'fecha_limite' && vacant[key]) {
          // Convertir fecha para input datetime-local
          const date = new Date(vacant[key]);
          setValue(key, date.toISOString().slice(0, 16));
        } else {
          setValue(key, vacant[key]);
        }
      });
    }
  }, [vacant, setValue]);

  const loadUsers = async () => {
    try {
      const response = await userService.getUsers(1, 50);
      setUsers(response.data.usuarios || []);
    } catch (error) {
      console.error('Error loading users:', error);
      toast.error('Error cargando usuarios');
    }
  };

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      
      // Convertir fecha límite si existe
      if (data.fecha_limite) {
        data.fecha_limite = new Date(data.fecha_limite).toISOString();
      }
      
      // Convertir números
      data.candidatos_requeridos = parseInt(data.candidatos_requeridos);
      data.entrevistas_op = parseInt(data.entrevistas_op);
      data.vacantes = parseInt(data.vacantes);
      
      if (data.salario_min) data.salario_min = parseFloat(data.salario_min);
      if (data.salario_max) data.salario_max = parseFloat(data.salario_max);

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

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-6">
        {vacant ? 'Editar Vacante' : 'Nueva Vacante'}
      </h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Información básica */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
              Ubicación
            </label>
            <input
              type="text"
              {...register('ubicacion')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ej: Felix Cuevas, CDMX"
            />
          </div>
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
            <select
              {...register('avance')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Creada">Creada</option>
              <option value="Buscando candidatos">Buscando candidatos</option>
              <option value="Candidatos enviados a RH">Candidatos enviados a RH</option>
              <option value="En proceso de entrevistas">En proceso de entrevistas</option>
              <option value="Seleccionando candidatos">Seleccionando candidatos</option>
              <option value="Posiciones cubiertas">Posiciones cubiertas</option>
              <option value="Finalizada">Finalizada</option>
            </select>
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
              <select
                {...register('reclutador_lider_id')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Seleccionar líder...</option>
                {reclutadoresLider.map(user => (
                  <option key={user.id} value={user.id}>
                    {user.nombre}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Detalles adicionales */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            📋 Detalles Adicionales
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Modalidad de Trabajo
              </label>
              <select
                {...register('modalidad')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="presencial">Presencial</option>
                <option value="remoto">Remoto</option>
                <option value="hibrido">Híbrido</option>
              </select>
            </div>

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
                Salario Mínimo
              </label>
              <input
                type="number"
                step="0.01"
                {...register('salario_min')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0.00"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Salario Máximo
              </label>
              <input
                type="number"
                step="0.01"
                {...register('salario_max')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0.00"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha Límite
              </label>
              <input
                type="datetime-local"
                {...register('fecha_limite')}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
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
        <div className="flex justify-end space-x-4 pt-6 border-t">
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
      </form>
    </div>
  );
};

export default VacantForm;
