import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen}
        currentPath={location.pathname}
      />
      
      {/* Contenido principal - Ahora se ajusta automáticamente al sidebar */}
      <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
        {/* Header */}
        <Header 
          setSidebarOpen={setSidebarOpen}
          currentPath={location.pathname}
        />
        
        {/* Contenido con padding responsivo */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <div className="p-4 lg:p-6">
            <div className="max-w-full">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;