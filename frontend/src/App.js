import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './hooks/useAuth';

// Componentes
import Layout from './components/Layout';
import ConnectionStatus from './components/ConnectionStatus';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clients from './pages/Clients';  // ⭐ NUEVO
import Vacants from './pages/Vacants';
import Candidates from './pages/Candidates';
import Interviews from './pages/Interviews';
import Users from './pages/Users';
import Reports from './pages/Reports';
import LoadingSpinner from './components/LoadingSpinner';

// Componente para rutas protegidas
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, connectionStatus } = useAuth();
  
  if (loading || connectionStatus === 'checking') {
    return <LoadingSpinner />;
  }
  
  // Si no hay conexión con el backend, mostrar mensaje de error
  if (connectionStatus === 'error') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <h2 className="text-lg font-semibold mb-2">❌ Error de Conexión</h2>
            <p className="mb-4">No se puede conectar con el servidor backend.</p>
            <p className="text-sm">
              Verifica que el servidor esté corriendo en{' '}
              <code className="bg-red-200 px-1 rounded">http://localhost:5000</code>
            </p>
          </div>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            🔄 Reintentar
          </button>
        </div>
      </div>
    );
  }
  
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Componente principal de rutas
const AppRoutes = () => {
  const { isAuthenticated, loading, connectionStatus } = useAuth();
  
  if (loading || connectionStatus === 'checking') {
    return <LoadingSpinner />;
  }
  
  return (
    <Routes>
      <Route 
        path="/login" 
        element={
          connectionStatus === 'error' ? (
            <div className="min-h-screen bg-gray-50 flex items-center justify-center">
              <div className="max-w-md mx-auto text-center">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                  <h2 className="text-lg font-semibold mb-2">❌ Error de Conexión</h2>
                  <p className="mb-4">No se puede conectar con el servidor backend.</p>
                  <button 
                    onClick={() => window.location.reload()}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                  >
                    🔄 Reintentar
                  </button>
                </div>
              </div>
            </div>
          ) : isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Login />
          )
        } 
      />
      
      <Route 
        path="/" 
        element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
      />
      
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/clients/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Clients />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/vacants/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Vacants />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/candidates/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Candidates />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/interviews/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Interviews />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/users/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Users />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/reports/*" 
        element={
          <ProtectedRoute>
            <Layout>
              <Reports />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <AppRoutes />
          <ConnectionStatus />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                theme: {
                  primary: 'green',
                  secondary: 'black',
                },
              },
            }}
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
