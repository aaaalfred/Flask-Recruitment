import { useState, useEffect, createContext, useContext } from 'react';
import { authService, testConnection } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState('checking'); // checking, connected, error

  // Verificar conexión con el backend al inicializar
  useEffect(() => {
    const checkBackendConnection = async () => {
      console.log('🔍 Verificando conexión con backend...');
      const result = await testConnection();
      
      if (result.success) {
        console.log('✅ Backend conectado exitosamente');
        setConnectionStatus('connected');
        toast.success('Conectado al servidor', { duration: 2000 });
      } else {
        console.error('❌ Error de conexión con backend:', result.error);
        setConnectionStatus('error');
        toast.error(`Error de conexión: ${result.error}`, { duration: 5000 });
      }
    };

    checkBackendConnection();
  }, []);

  // Verificar token almacenado al inicializar
  useEffect(() => {
    const initializeAuth = async () => {
      console.log('🔐 Inicializando autenticación...');
      
      const token = localStorage.getItem('authToken');
      const userInfo = localStorage.getItem('userInfo');
      
      if (token && userInfo) {
        try {
          const parsedUser = JSON.parse(userInfo);
          console.log('👤 Usuario encontrado en localStorage:', parsedUser.email);
          
          // Verificar si el token es válido (opcional)
          // const tokenValid = await authService.verifyToken();
          // if (!tokenValid.success) {
          //   throw new Error('Token inválido');
          // }
          
          setUser(parsedUser);
          console.log('✅ Sesión restaurada exitosamente');
        } catch (error) {
          console.error('❌ Error restaurando sesión:', error);
          localStorage.removeItem('authToken');
          localStorage.removeItem('userInfo');
          setUser(null);
        }
      } else {
        console.log('ℹ️ No hay sesión previa');
      }
      
      setLoading(false);
    };

    // Solo inicializar auth si hay conexión con backend
    if (connectionStatus === 'connected') {
      initializeAuth();
    } else if (connectionStatus === 'error') {
      setLoading(false);
    }
  }, [connectionStatus]);

  const login = async (credentials) => {
    try {
      setLoading(true);
      console.log('🔑 Intentando login para:', credentials.email);
      
      const response = await authService.login(credentials);
      const { access_token, user: userData } = response.data;
      
      console.log('✅ Login exitoso:', userData);
      
      localStorage.setItem('authToken', access_token);
      localStorage.setItem('userInfo', JSON.stringify(userData));
      setUser(userData);
      
      toast.success(`¡Bienvenido, ${userData.nombre}!`);
      return { success: true };
    } catch (error) {
      console.error('❌ Error en login:', error);
      const message = error.response?.data?.message || 'Error al iniciar sesión';
      toast.error(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    console.log('👋 Cerrando sesión...');
    authService.logout();
    setUser(null);
    toast.success('Sesión cerrada exitosamente');
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      console.log('📝 Registrando usuario:', userData.email);
      
      await authService.register(userData);
      toast.success('Usuario registrado exitosamente');
      return { success: true };
    } catch (error) {
      console.error('❌ Error en registro:', error);
      const message = error.response?.data?.message || 'Error al registrar usuario';
      toast.error(message);
      return { success: false, error: message };
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    login,
    logout,
    register,
    loading,
    isAuthenticated: !!user,
    connectionStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
