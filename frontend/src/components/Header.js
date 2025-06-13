import React, { Fragment } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Menu, Transition } from '@headlessui/react';
import { 
  Bars3Icon,
  BellIcon,
  UserCircleIcon,
  ChevronDownIcon
} from '@heroicons/react/24/outline';
import { getInitials, getAvatarColor } from '../utils/helpers';

const Header = ({ setSidebarOpen, currentPath }) => {
  const { user, logout } = useAuth();

  const getPageTitle = (path) => {
    const titles = {
      '/dashboard': 'Dashboard',
      '/vacants': 'Gestión de Vacantes',
      '/candidates': 'Gestión de Candidatos', 
      '/interviews': 'Entrevistas',
      '/users': 'Gestión de Usuarios',
      '/reports': 'Reportes y Análisis'
    };
    
    for (const [route, title] of Object.entries(titles)) {
      if (path.startsWith(route)) {
        return title;
      }
    }
    return 'Sistema RH';
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Lado izquierdo */}
        <div className="flex items-center">
          {/* Botón menú móvil */}
          <button
            type="button"
            className="lg:hidden p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
            onClick={() => setSidebarOpen(true)}
          >
            <Bars3Icon className="h-6 w-6" />
          </button>
          
          {/* Título de página */}
          <h1 className="ml-4 lg:ml-0 text-2xl font-semibold text-gray-900">
            {getPageTitle(currentPath)}
          </h1>
        </div>

        {/* Lado derecho */}
        <div className="flex items-center space-x-4">
          {/* Notificaciones */}
          <button
            type="button"
            className="p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500 relative"
          >
            <BellIcon className="h-6 w-6" />
            {/* Badge de notificaciones */}
            <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white" />
          </button>

          {/* Menú de usuario */}
          <Menu as="div" className="relative">
            <Menu.Button className="flex items-center space-x-3 p-2 rounded-md text-sm hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500">
              {/* Avatar */}
              <div className={`h-8 w-8 rounded-full ${getAvatarColor(user?.nombre)} flex items-center justify-center text-white text-sm font-medium`}>
                {getInitials(user?.nombre)}
              </div>
              
              {/* Info usuario */}
              <div className="hidden lg:block text-left">
                <p className="text-sm font-medium text-gray-700">{user?.nombre}</p>
                <p className="text-xs text-gray-500 capitalize">{user?.rol?.replace('_', ' ')}</p>
              </div>
              
              <ChevronDownIcon className="h-4 w-4 text-gray-500" />
            </Menu.Button>

            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <a
                        href="#"
                        className={`${
                          active ? 'bg-gray-100' : ''
                        } flex items-center px-4 py-2 text-sm text-gray-700`}
                      >
                        <UserCircleIcon className="h-4 w-4 mr-3" />
                        Mi Perfil
                      </a>
                    )}
                  </Menu.Item>
                  
                  <div className="border-t border-gray-100"></div>
                  
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        onClick={logout}
                        className={`${
                          active ? 'bg-gray-100' : ''
                        } flex items-center w-full text-left px-4 py-2 text-sm text-gray-700`}
                      >
                        <svg className="h-4 w-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        Cerrar Sesión
                      </button>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </header>
  );
};

export default Header;
