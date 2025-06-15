import React, { useState, useEffect } from 'react';
import { reportService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      console.log('🔄 Cargando estadísticas del dashboard...');
      const response = await reportService.getDashboardStats();
      setStats(response.data);
      console.log('📊 Estadísticas cargadas exitosamente:', response.data);
      toast.success('Estadísticas actualizadas');
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
      if (error.code === 'ECONNABORTED') {
        toast.error('El servidor está tardando en responder. Reintentando...');
        // Reintentar una vez más
        setTimeout(() => loadDashboardStats(), 2000);
      } else {
        toast.error('Error cargando estadísticas del dashboard');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">📊 Cargando estadísticas...</p>
          <p className="text-sm text-gray-500">Esto puede tomar unos segundos</p>
        </div>
      </div>
    );
  }

  const getEstadoColor = (estado) => {
    const colores = {
      'postulado': 'bg-blue-100 text-blue-800',
      'en_proceso': 'bg-yellow-100 text-yellow-800',
      'seleccionado': 'bg-green-100 text-green-800',
      'rechazado': 'bg-red-100 text-red-800',
      'descartado': 'bg-gray-100 text-gray-800'
    };
    return colores[estado] || 'bg-gray-100 text-gray-800';
  };

  const getPrioridadIcon = (prioridad) => {
    const iconos = {
      'critica': '🔴',
      'alta': '🟠',
      'media': '🟡',
      'baja': '🟢'
    };
    return iconos[prioridad] || '⚪';
  };

  const getModalidadIcon = (modalidad) => {
    const iconos = {
      'presencial': '🏢',
      'remoto': '💻',
      'hibrido': '🔄'
    };
    return iconos[modalidad] || '📍';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              📊 Dashboard de Reclutamiento
            </h1>
            <p className="text-gray-600">
              Resumen general del proceso de reclutamiento - {user?.rol} 
            </p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-500">
              Última actualización: {stats?.fecha_actualizacion ? 
                new Date(stats.fecha_actualizacion).toLocaleString() : 'N/A'
              }
            </p>
            <button
              onClick={loadDashboardStats}
              className="mt-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : '🔄 Actualizar'}
            </button>
          </div>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        <div className="bg-white rounded-lg shadow-md p-4 lg:p-6">
          <div className="flex items-center">
            <div className="p-2 lg:p-3 rounded-full bg-blue-100 text-blue-600 text-lg lg:text-xl">
              🎯
            </div>
            <div className="ml-3 lg:ml-4 min-w-0 flex-1">
              <p className="text-xs lg:text-sm font-medium text-gray-500 truncate">Total Vacantes</p>
              <p className="text-lg lg:text-2xl font-semibold text-gray-900">
                {stats?.total_vacantes || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4 lg:p-6">
          <div className="flex items-center">
            <div className="p-2 lg:p-3 rounded-full bg-green-100 text-green-600 text-lg lg:text-xl">
              ✅
            </div>
            <div className="ml-3 lg:ml-4 min-w-0 flex-1">
              <p className="text-xs lg:text-sm font-medium text-gray-500 truncate">Vacantes Abiertas</p>
              <p className="text-lg lg:text-2xl font-semibold text-gray-900">
                {stats?.vacantes_abiertas || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4 lg:p-6">
          <div className="flex items-center">
            <div className="p-2 lg:p-3 rounded-full bg-purple-100 text-purple-600 text-lg lg:text-xl">
              👥
            </div>
            <div className="ml-3 lg:ml-4 min-w-0 flex-1">
              <p className="text-xs lg:text-sm font-medium text-gray-500 truncate">Total Candidatos</p>
              <p className="text-lg lg:text-2xl font-semibold text-gray-900">
                {stats?.total_candidatos || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4 lg:p-6">
          <div className="flex items-center">
            <div className="p-2 lg:p-3 rounded-full bg-orange-100 text-orange-600 text-lg lg:text-xl">
              📅
            </div>
            <div className="ml-3 lg:ml-4 min-w-0 flex-1">
              <p className="text-xs lg:text-sm font-medium text-gray-500 truncate">Entrevistas Pendientes</p>
              <p className="text-lg lg:text-2xl font-semibold text-gray-900">
                {stats?.entrevistas_pendientes || 0}
              </p>
            </div>
          </div>
        </div>
      </div>
      {/* Estadísticas de Estados y Distribuciones */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        
        {/* Candidatos por Estado */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            👥 Candidatos por Estado
          </h2>
          <div className="space-y-3">
            {stats?.candidatos_por_estado && Object.entries(stats.candidatos_por_estado).map(([estado, count]) => (
              <div key={estado} className="flex items-center justify-between">
                <div className="flex items-center">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getEstadoColor(estado)}`}>
                    {estado || 'Sin estado'}
                  </span>
                </div>
                <span className="font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Vacantes por Prioridad */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            🎯 Vacantes por Prioridad
          </h2>
          <div className="space-y-3">
            {stats?.vacantes_por_prioridad && Object.entries(stats.vacantes_por_prioridad).map(([prioridad, count]) => (
              <div key={prioridad} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{getPrioridadIcon(prioridad)}</span>
                  <span className="text-sm font-medium text-gray-700">
                    {prioridad || 'Sin prioridad'}
                  </span>
                </div>
                <span className="font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Vacantes por Modalidad */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            📍 Vacantes por Modalidad
          </h2>
          <div className="space-y-3">
            {stats?.vacantes_por_modalidad && Object.entries(stats.vacantes_por_modalidad).map(([modalidad, count]) => (
              <div key={modalidad} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{getModalidadIcon(modalidad)}</span>
                  <span className="text-sm font-medium text-gray-700">
                    {modalidad || 'Sin modalidad'}
                  </span>
                </div>
                <span className="font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Actividad Reciente y Resumen de Estados */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        
        {/* Actividad Reciente */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            📈 Actividad Reciente (7 días)
          </h2>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-blue-600">Candidatos Nuevos</p>
                  <p className="text-2xl font-bold text-blue-700">
                    {stats?.candidatos_recientes || 0}
                  </p>
                </div>
                <div className="text-2xl">👤</div>
              </div>
            </div>

            <div className="bg-purple-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-purple-600">Entrevistas</p>
                  <p className="text-2xl font-bold text-purple-700">
                    {stats?.entrevistas_recientes || 0}
                  </p>
                </div>
                <div className="text-2xl">📅</div>
              </div>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-3 gap-2 text-center">
            <div className="bg-gray-50 rounded p-2">
              <p className="text-xs text-gray-500">Cerradas</p>
              <p className="font-semibold text-gray-700">{stats?.vacantes_cerradas || 0}</p>
            </div>
            <div className="bg-gray-50 rounded p-2">
              <p className="text-xs text-gray-500">Pausadas</p>
              <p className="font-semibold text-gray-700">{stats?.vacantes_pausadas || 0}</p>
            </div>
            <div className="bg-gray-50 rounded p-2">
              <p className="text-xs text-gray-500">Canceladas</p>
              <p className="font-semibold text-gray-700">{stats?.vacantes_canceladas || 0}</p>
            </div>
          </div>
        </div>

        {/* Estadísticas de Entrevistas */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            📊 Resumen de Entrevistas
          </h2>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <span className="text-lg">⏳</span>
                <span className="font-medium text-yellow-800">Pendientes</span>
              </div>
              <span className="text-xl font-bold text-yellow-700">
                {stats?.entrevistas_pendientes || 0}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <span className="text-lg">✅</span>
                <span className="font-medium text-green-800">Aprobadas</span>
              </div>
              <span className="text-xl font-bold text-green-700">
                {stats?.entrevistas_aprobadas || 0}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div className="flex items-center space-x-2">
                <span className="text-lg">❌</span>
                <span className="font-medium text-red-800">Rechazadas</span>
              </div>
              <span className="text-xl font-bold text-red-700">
                {stats?.entrevistas_rechazadas || 0}
              </span>
            </div>
          </div>

          {/* Entrevistas por Tipo */}
          {stats?.entrevistas_por_tipo && Object.keys(stats.entrevistas_por_tipo).length > 0 && (
            <div className="mt-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Por Tipo:</h3>
              <div className="space-y-1">
                {Object.entries(stats.entrevistas_por_tipo).map(([tipo, count]) => (
                  <div key={tipo} className="flex justify-between text-sm">
                    <span className="text-gray-600">{tipo}</span>
                    <span className="font-medium">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Vacantes que Requieren Atención */}
      {stats?.vacantes_antiguas && stats.vacantes_antiguas.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            ⚠️ Vacantes que Requieren Atención
          </h2>
          
          <div className="space-y-3">
            {stats.vacantes_antiguas.slice(0, 5).map((vacante) => (
              <div key={vacante.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getPrioridadIcon(vacante.prioridad)}</span>
                    <p className="font-medium text-gray-900 truncate">
                      {vacante.nombre}
                    </p>
                  </div>
                  <p className="text-sm text-gray-500">
                    {vacante.ejecutivo} • {vacante.candidatos} candidatos
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    {vacante.dias_transcurridos} días
                  </p>
                  <p className="text-xs text-gray-500">abierta</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Rendimiento por Reclutador (solo para ejecutivos y líderes) */}
      {stats?.rendimiento_reclutadores && stats.rendimiento_reclutadores.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-4 lg:p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            🏆 Rendimiento por Reclutador
          </h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Reclutador
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vacantes
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Candidatos
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Entrevistas
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Seleccionados
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Efectividad
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.rendimiento_reclutadores.map((reclutador, index) => (
                  <tr key={index}>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900 text-sm">{reclutador.nombre}</div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {reclutador.vacantes}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {reclutador.candidatos}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {reclutador.entrevistas}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                      {reclutador.seleccionados}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        reclutador.efectividad >= 50 ? 'bg-green-100 text-green-800' :
                        reclutador.efectividad >= 25 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {reclutador.efectividad}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Estadísticas de Usuarios (solo para ejecutivos y líderes) */}
      {stats?.usuarios && Object.keys(stats.usuarios).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            👤 Estadísticas de Usuarios
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">
                {stats.usuarios.total_usuarios || 0}
              </p>
              <p className="text-sm text-gray-500">Total Usuarios</p>
            </div>
            
            {stats.usuarios.por_rol && Object.entries(stats.usuarios.por_rol).map(([rol, count]) => (
              <div key={rol} className="text-center">
                <p className="text-2xl font-bold text-gray-700">{count}</p>
                <p className="text-sm text-gray-500 capitalize">{rol.replace('_', ' ')}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resumen de Estados */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Candidatos Activos</p>
              <p className="text-xl font-semibold text-gray-900">
                {stats?.candidatos_activos || 0}
              </p>
            </div>
            <div className="p-2 rounded-full bg-green-100 text-green-600 text-lg">
              ✅
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Candidatos Inactivos</p>
              <p className="text-xl font-semibold text-gray-900">
                {stats?.candidatos_inactivos || 0}
              </p>
            </div>
            <div className="p-2 rounded-full bg-gray-100 text-gray-600 text-lg">
              ⏸️
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Total Entrevistas</p>
              <p className="text-xl font-semibold text-gray-900">
                {stats?.total_entrevistas || 0}
              </p>
            </div>
            <div className="p-2 rounded-full bg-purple-100 text-purple-600 text-lg">
              📋
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Tasa de Conversión</p>
              <p className="text-xl font-semibold text-gray-900">
                {stats?.total_candidatos > 0 && stats?.rendimiento_reclutadores ? 
                  ((stats.rendimiento_reclutadores.reduce((sum, r) => sum + r.seleccionados, 0) / stats.total_candidatos) * 100).toFixed(1)
                  : 0}%
              </p>
            </div>
            <div className="p-2 rounded-full bg-indigo-100 text-indigo-600 text-lg">
              📊
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
