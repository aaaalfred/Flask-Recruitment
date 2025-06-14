import React, { useState, useEffect } from 'react';
import { reportService, vacantService } from '../services/api';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      const response = await vacantService.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading dashboard stats:', error);
      toast.error('Error cargando estadísticas del dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

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

  const getPriorityIcon = (dias) => {
    if (dias > 100) return '🔴';
    if (dias > 60) return '🟡';
    if (dias > 30) return '🟠';
    return '🟢';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">
          📊 Dashboard de Reclutamiento
        </h1>
        <p className="text-gray-600">
          Resumen general del proceso de reclutamiento y vacantes activas
        </p>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100 text-blue-600">
              🎯
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Vacantes</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.total_vacantes || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-100 text-green-600">
              ✅
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Vacantes Abiertas</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.vacantes_abiertas || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-100 text-purple-600">
              👥
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Candidatos</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.total_candidatos || 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-orange-100 text-orange-600">
              ⭐
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Seleccionados</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.candidatos_seleccionados || 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Estado de avance y vacantes antiguas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Estado por avance */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            📈 Estado por Avance
          </h2>
          
          <div className="space-y-3">
            {stats?.por_avance && Object.entries(stats.por_avance).map(([avance, count]) => (
              <div key={avance} className="flex items-center justify-between">
                <div className="flex items-center">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAvanceColor(avance)}`}>
                    {avance || 'Sin avance'}
                  </span>
                </div>
                <span className="font-semibold text-gray-900">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Vacantes más antiguas */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            ⏰ Vacantes que Requieren Atención
          </h2>
          
          <div className="space-y-3">
            {stats?.vacantes_antiguas?.slice(0, 5).map((vacante, index) => (
              <div key={vacante.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <p className="font-medium text-gray-900 truncate">
                    {getPriorityIcon(vacante.dias_transcurridos)} {vacante.nombre}
                  </p>
                  <p className="text-sm text-gray-500">
                    {vacante.ejecutivo} • {vacante.candidatos} candidatos
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    {vacante.dias_transcurridos} días
                  </p>
                </div>
              </div>
            )) || (
              <p className="text-gray-500 text-center py-4">
                No hay vacantes para mostrar
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Estadísticas por reclutador */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          👤 Rendimiento por Reclutador
        </h2>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reclutador
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Vacantes
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Candidatos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Seleccionados
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Efectividad
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats?.por_reclutador && Object.entries(stats.por_reclutador).map(([reclutador, data]) => {
                const efectividad = data.candidatos > 0 ? ((data.seleccionados / data.candidatos) * 100).toFixed(1) : 0;
                
                return (
                  <tr key={reclutador}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-medium text-gray-900">{reclutador}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.vacantes}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.candidatos}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {data.seleccionados}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        efectividad >= 50 ? 'bg-green-100 text-green-800' :
                        efectividad >= 25 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {efectividad}%
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Métricas adicionales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Vacantes Cerradas</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.vacantes_cerradas || 0}
              </p>
            </div>
            <div className="p-3 rounded-full bg-gray-100 text-gray-600">
              🔒
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Propuestas Totales</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.propuestas_totales || 0}
              </p>
            </div>
            <div className="p-3 rounded-full bg-yellow-100 text-yellow-600">
              📄
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Tasa de Conversión</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats?.total_candidatos > 0 
                  ? ((stats.candidatos_seleccionados / stats.total_candidatos) * 100).toFixed(1)
                  : 0}%
              </p>
            </div>
            <div className="p-3 rounded-full bg-indigo-100 text-indigo-600">
              📊
            </div>
          </div>
        </div>
      </div>

      {/* Botón de actualización */}
      <div className="flex justify-center">
        <button
          onClick={loadDashboardStats}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        >
          {loading ? 'Actualizando...' : '🔄 Actualizar Datos'}
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
