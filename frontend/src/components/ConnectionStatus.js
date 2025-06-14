import React, { useState, useEffect } from 'react';
import { testConnection } from '../services/api';

const ConnectionStatus = () => {
  const [status, setStatus] = useState('checking');
  const [details, setDetails] = useState(null);
  const [lastCheck, setLastCheck] = useState(null);

  const checkConnection = async () => {
    setStatus('checking');
    console.log('🔍 Verificando conexión...');
    
    const result = await testConnection();
    
    if (result.success) {
      setStatus('connected');
      setDetails(result.data);
      console.log('✅ Conexión exitosa');
    } else {
      setStatus('error');
      setDetails({ error: result.error });
      console.error('❌ Error de conexión:', result.error);
    }
    
    setLastCheck(new Date());
  };

  useEffect(() => {
    checkConnection();
    
    // Verificar conexión cada 30 segundos
    const interval = setInterval(checkConnection, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusInfo = () => {
    switch (status) {
      case 'checking':
        return {
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
          icon: '🔍',
          text: 'Verificando conexión...'
        };
      case 'connected':
        return {
          color: 'text-green-600',
          bgColor: 'bg-green-100',
          icon: '✅',
          text: 'Conectado al servidor'
        };
      case 'error':
        return {
          color: 'text-red-600',
          bgColor: 'bg-red-100',
          icon: '❌',
          text: 'Error de conexión'
        };
      default:
        return {
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
          icon: '❓',
          text: 'Estado desconocido'
        };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div className={`fixed bottom-4 right-4 p-3 rounded-lg shadow-lg ${statusInfo.bgColor} ${statusInfo.color} max-w-xs z-50`}>
      <div className="flex items-center space-x-2">
        <span>{statusInfo.icon}</span>
        <div className="flex-1">
          <p className="text-sm font-medium">{statusInfo.text}</p>
          {lastCheck && (
            <p className="text-xs opacity-70">
              Última verificación: {lastCheck.toLocaleTimeString()}
            </p>
          )}
        </div>
        <button
          onClick={checkConnection}
          className="text-xs underline hover:no-underline"
          disabled={status === 'checking'}
        >
          Verificar
        </button>
      </div>
      
      {details && status === 'connected' && (
        <div className="mt-2 text-xs">
          <p>Servidor: {details.message}</p>
          <p>Versión: {details.version}</p>
        </div>
      )}
      
      {details && status === 'error' && (
        <div className="mt-2 text-xs">
          <p>Error: {details.error}</p>
          <p className="mt-1 text-xs opacity-70">
            Verifica que el backend esté corriendo en http://localhost:5000
          </p>
        </div>
      )}
    </div>
  );
};

export default ConnectionStatus;
