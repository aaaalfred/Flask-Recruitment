import React, { useState, useEffect } from 'react';
import { reportService } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('general');
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
      toast.success('Dashboard actualizado');
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
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg text-gray-600">📊 Cargando dashboard...</p>
          <p className="text-sm text-gray-500">Generando estadísticas mejoradas...</p>
        </div>
      </div>
    );
  }

  const getStatusColor = (status) => {
    const colors = {
      'postulado': 'bg-blue-100 text-blue-800',
      'en_proceso': 'bg-yellow-100 text-yellow-800',
      'aceptado': 'bg-green-100 text-green-800',
      'rechazado': 'bg-red-100 text-red-800',
      'contratado': 'bg-emerald-100 text-emerald-800',
      'pendiente': 'bg-orange-100 text-orange-800',
      'no_contratable': 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityIcon = (priority) => {
    const icons = {
      'critica': '🔴',
      'alta': '🟠', 
      'media': '🟡',
      'baja': '🟢'
    };
    return icons[priority] || '⚪';
  };

  const renderMetricCard = (title, value, icon, color = 'blue', subtitle = null) => (
    <div className="bg-white rounded-lg shadow-md p-4 lg:p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center">
        <div className={`p-2 lg:p-3 rounded-full bg-${color}-100 text-${color}-600 text-lg lg:text-xl`}>
          {icon}
        </div>
        <div className="ml-3 lg:ml-4 min-w-0 flex-1">
          <p className="text-xs lg:text-sm font-medium text-gray-500 truncate">{title}</p>
          <p className="text-lg lg:text-2xl font-semibold text-gray-900">
            {typeof value === 'number' ? value.toLocaleString() : value}
          </p>
          {subtitle && (
            <p className="text-xs text-gray-400">{subtitle}</p>
          )}
        </div>
      </div>
    </div>
  );

  const TabButton = ({ id, label, icon, isActive, onClick, badge = null }) => (
    <button
      onClick={() => onClick(id)}
      className={`relative flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${
        isActive 
          ? 'bg-blue-600 text-white' 
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      <span className="mr-2">{icon}</span>
      {label}
      {badge && (
        <span className={`ml-2 px-2 py-1 text-xs rounded-full ${
          isActive ? 'bg-blue-400 text-white' : 'bg-red-500 text-white'
        }`}>
          {badge}
        </span>
      )}
    </button>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              📊 Dashboard de Reclutamiento Mejorado
            </h1>
            <p className="text-gray-600">
              Panel de control integral - {user?.rol} 
              {stats?.filtrado_por_reclutador && ' (Vista personalizada)'}
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
              className="mt-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
              disabled={loading}
            >
              {loading ? 'Actualizando...' : '🔄 Actualizar'}
            </button>
          </div>
        </div>
      </div>

      {/* Navegación por pestañas */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex flex-wrap gap-2">
          <TabButton
            id="general"
            label="General"
            icon="📊"
            isActive={activeTab === 'general'}
            onClick={setActiveTab}
          />
          <TabButton
            id="proceso"
            label="Proceso"
            icon="🔄"
            isActive={activeTab === 'proceso'}
            onClick={setActiveTab}
          />
          {stats?.clientes_stats?.length > 0 && (
            <TabButton
              id="clientes"
              label="Clientes"
              icon="🏢"
              isActive={activeTab === 'clientes'}
              onClick={setActiveTab}
              badge={stats.clientes_stats.length}
            />
          )}
          {stats?.rendimiento_reclutadores?.length > 0 && (
            <TabButton
              id="equipo"
              label="Equipo"
              icon="👥"
              isActive={activeTab === 'equipo'}
              onClick={setActiveTab}
            />
          )}
          {stats?.vacantes_antiguas?.length > 0 && (
            <TabButton
              id="alertas"
              label="Alertas"
              icon="⚠️"
              isActive={activeTab === 'alertas'}
              onClick={setActiveTab}
              badge={stats.vacantes_antiguas.length}
            />
          )}
        </div>
      </div>

      {/* Contenido según pestaña activa */}
      {activeTab === 'general' && (
        <>
          {/* Métricas principales */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
            {renderMetricCard('Total Vacantes', stats?.total_vacantes || 0, '🎯', 'blue')}
            {renderMetricCard('Vacantes Abiertas', stats?.vacantes_abiertas || 0, '✅', 'green')}
            {renderMetricCard('Total Candidatos', stats?.total_candidatos || 0, '👥', 'purple')}
            {renderMetricCard('Entrevistas Pendientes', stats?.entrevistas_pendientes || 0, '📅', 'orange')}
          </div>

          {/* Métricas de rendimiento */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {renderMetricCard('Vacantes Cubiertas', stats?.vacantes_cubiertas || 0, '🏆', 'emerald', 'Posiciones completadas')}
            {renderMetricCard('Candidatos Aceptados', stats?.candidatos_aceptados_supervisor || 0, '✨', 'cyan', 'Por supervisor')}
            {renderMetricCard('Tasa de Conversión', `${stats?.tasa_conversion_global || 0}%`, '📊', 'indigo', 'Global del proceso')}
            {renderMetricCard('Tiempo Prom. Resolución', `${stats?.tiempo_promedio_resolucion || 0} días`, '⏱️', 'gray', 'Para cubrir vacantes')}
          </div>

          {/* Actividad reciente */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">📈 Actividad Reciente (7 días)</h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-blue-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-700">{stats?.vacantes_recientes || 0}</div>
                <div className="text-sm text-blue-600">Vacantes Nuevas</div>
              </div>
              <div className="bg-purple-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-700">{stats?.candidatos_recientes || 0}</div>
                <div className="text-sm text-purple-600">Candidatos Nuevos</div>
              </div>
              <div className="bg-orange-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-orange-700">{stats?.entrevistas_recientes || 0}</div>
                <div className="text-sm text-orange-600">Entrevistas</div>
              </div>
            </div>
          </div>
        </>
      )}

      {activeTab === 'proceso' && (
        <>
          {/* Distribuciones del proceso */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Candidatos por Status */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">👥 Candidatos por Status</h2>
              <div className="space-y-3">
                {stats?.candidatos_por_status && Object.entries(stats.candidatos_por_status).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
                      {status?.replace('_', ' ') || 'Sin status'}
                    </span>
                    <span className="font-semibold text-gray-900">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Candidatos por Status de Contratación */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">📋 Status de Contratación</h2>
              <div className="space-y-3">
                {stats?.candidatos_por_contratacion && Object.entries(stats.candidatos_por_contratacion).map(([status, count]) => (
                  <div key={status} className="flex items-center justify-between">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
                      {status?.replace('_', ' ') || 'Sin status'}
                    </span>
                    <span className="font-semibold text-gray-900">{count}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Vacantes por Prioridad */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">🎯 Vacantes por Prioridad</h2>
              <div className="space-y-3">
                {stats?.vacantes_por_prioridad && Object.entries(stats.vacantes_por_prioridad).map(([priority, count]) => (
                  <div key={priority} className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">{getPriorityIcon(priority)}</span>
                      <span className="text-sm font-medium text-gray-700">
                        {priority || 'Sin prioridad'}
                      </span>
                    </div>
                    <span className="font-semibold text-gray-900">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Entrevistas y modalidades */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Entrevistas por tipo */}
            {stats?.entrevistas_por_tipo && Object.keys(stats.entrevistas_por_tipo).length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">📞 Entrevistas por Tipo</h2>
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(stats.entrevistas_por_tipo).map(([tipo, count]) => (
                    <div key={tipo} className="text-center p-3 bg-gray-50 rounded-lg">
                      <div className="text-lg font-bold text-gray-700">{count}</div>
                      <div className="text-xs text-gray-500 capitalize">{tipo}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Vacantes por modalidad */}
            {stats?.vacantes_por_modalidad && Object.keys(stats.vacantes_por_modalidad).length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">📍 Vacantes por Modalidad</h2>
                <div className="space-y-3">
                  {Object.entries(stats.vacantes_por_modalidad).map(([modalidad, count]) => (
                    <div key={modalidad} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-lg">
                          {modalidad === 'presencial' ? '🏢' : modalidad === 'remoto' ? '💻' : '🔄'}
                        </span>
                        <span className="text-sm font-medium text-gray-700">
                          {modalidad || 'Sin modalidad'}
                        </span>
                      </div>
                      <span className="font-semibold text-gray-900">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </>
      )}

      {activeTab === 'clientes' && stats?.clientes_stats?.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">🏢 Análisis por Cliente</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">CCP</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vacantes</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cubiertas</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tasa Éxito</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {stats.clientes_stats.map((cliente, index) => (
                  <tr key={index} className={index < 3 ? 'bg-green-50' : ''}>
                    <td className="px-4 py-4 whitespace-nowrap font-medium text-gray-900">
                      {index < 3 && <span className="mr-2">🏆</span>}
                      {cliente.nombre}
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-500">{cliente.ccp}</td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{cliente.total_vacantes}</td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{cliente.vacantes_cubiertas}</td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        cliente.tasa_exito >= 50 ? 'bg-green-100 text-green-800' :
                        cliente.tasa_exito >= 25 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {cliente.tasa_exito}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'equipo' && stats?.rendimiento_reclutadores?.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">🏆 Rendimiento del Equipo</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reclutador</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vacantes</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Candidatos</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contratados</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Efectividad</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actividad 7d</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.rendimiento_reclutadores.map((reclutador, index) => (
                  <tr key={index} className={index < 3 ? 'bg-yellow-50' : ''}>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {index < 3 && <span className="mr-2">🥇</span>}
                        <div className="font-medium text-gray-900 text-sm">{reclutador.nombre}</div>
                      </div>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{reclutador.vacantes_asignadas}</td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{reclutador.candidatos_gestionados}</td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{reclutador.candidatos_contratados}</td>
                    <td className="px-4 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        reclutador.efectividad_final >= 50 ? 'bg-green-100 text-green-800' :
                        reclutador.efectividad_final >= 25 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {reclutador.efectividad_final}%
                      </span>
                    </td>
                    <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-900">{reclutador.actividad_reciente}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'alertas' && stats?.vacantes_antiguas?.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">⚠️ Vacantes que Requieren Atención</h2>
          <div className="space-y-4">
            {stats.vacantes_antiguas.map((vacante) => (
              <div key={vacante.id} className="flex items-center justify-between p-4 bg-amber-50 rounded-lg border border-amber-200">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getPriorityIcon(vacante.prioridad)}</span>
                    <div>
                      <p className="font-medium text-gray-900">{vacante.nombre}</p>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <span>Cliente: {vacante.cliente_nombre}</span>
                        <span>CCP: {vacante.cliente_ccp}</span>
                        <span>Ejecutivo: {vacante.ejecutivo}</span>
                      </div>
                      <div className="flex items-center space-x-4 text-xs text-gray-500 mt-1">
                        <span>Candidatos: {vacante.candidatos_actuales}/{vacante.candidatos_requeridos}</span>
                        <span className={vacante.candidatos_faltantes > 0 ? 'text-red-600 font-medium' : 'text-green-600'}>
                          {vacante.candidatos_faltantes > 0 ? `Faltan: ${vacante.candidatos_faltantes}` : 'Completo'}
                        </span>
                        <span>Avance: {vacante.avance}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-amber-700">{vacante.dias_transcurridos} días</p>
                  <p className="text-xs text-amber-600">sin cubrir</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resumen de Estados */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {renderMetricCard('Candidatos Activos', stats?.candidatos_activos || 0, '✅', 'green')}
        {renderMetricCard('Candidatos Inactivos', stats?.candidatos_inactivos || 0, '⏸️', 'gray')}
        {renderMetricCard('Total Entrevistas', stats?.total_entrevistas || 0, '📋', 'purple')}
        {renderMetricCard('Blacklist', stats?.candidatos_blacklist || 0, '🚫', 'red')}
      </div>

      {/* Estadísticas de Usuarios (solo para supervisores) */}
      {stats?.usuarios && Object.keys(stats.usuarios).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">👤 Estadísticas del Equipo</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-2xl font-bold text-blue-600">{stats.usuarios.total_usuarios || 0}</p>
              <p className="text-sm text-blue-700">Total Usuarios</p>
            </div>
            
            {stats.usuarios.por_rol && Object.entries(stats.usuarios.por_rol).map(([rol, count]) => (
              <div key={rol} className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-2xl font-bold text-gray-700">{count}</p>
                <p className="text-sm text-gray-600 capitalize">{rol.replace('_', ' ')}</p>
              </div>
            ))}
          </div>
          
          {stats.usuarios.usuarios_recientes > 0 && (
            <div className="mt-4 p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-700">
                <span className="font-medium">{stats.usuarios.usuarios_recientes}</span> usuarios nuevos esta semana
              </p>
            </div>
          )}
        </div>
      )}

      {/* Footer con información adicional */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div>
            <span className="font-medium">Sistema de Reclutamiento</span> | 
            Dashboard v2.0 con análisis mejorado
          </div>
          <div>
            Generado para: {stats?.usuario_nombre} | Datos: {new Date(stats?.fecha_actualizacion || new Date()).toLocaleString()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;