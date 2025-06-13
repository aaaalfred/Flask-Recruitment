import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';
import { Dialog, Transition } from '@headlessui/react';
import { useAuth } from '../hooks/useAuth';
import { 
  XMarkIcon,
  HomeIcon,
  BriefcaseIcon,
  UserGroupIcon,
  CalendarDaysIcon,
  UsersIcon,
  ChartBarIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';

const Sidebar = ({ sidebarOpen, setSidebarOpen, currentPath }) => {
  const { user } = useAuth();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon, roles: ['ejecutivo', 'reclutador', 'reclutador_lider'] },
    { name: 'Vacantes', href: '/vacants', icon: BriefcaseIcon, roles: ['ejecutivo', 'reclutador', 'reclutador_lider'] },
    { name: 'Candidatos', href: '/candidates', icon: UserGroupIcon, roles: ['ejecutivo', 'reclutador', 'reclutador_lider'] },
    { name: 'Entrevistas', href: '/interviews', icon: CalendarDaysIcon, roles: ['ejecutivo', 'reclutador', 'reclutador_lider'] },
    { name: 'Usuarios', href: '/users', icon: UsersIcon, roles: ['ejecutivo', 'reclutador_lider'] },
    { name: 'Reportes', href: '/reports', icon: ChartBarIcon, roles: ['ejecutivo', 'reclutador_lider'] },
  ];

  const filteredNavigation = navigation.filter(item => 
    item.roles.includes(user?.rol)
  );

  const isActive = (href) => {
    return currentPath.startsWith(href);
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center justify-center h-16 px-4 bg-primary-600">
        <div className="flex items-center space-x-2">
          <BuildingOfficeIcon className="h-8 w-8 text-white" />
          <span className="text-white text-xl font-bold">Sistema RH</span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1 bg-white">
        {filteredNavigation.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.name}
              to={item.href}
              onClick={() => setSidebarOpen(false)}
              className={`${
                isActive(item.href)
                  ? 'bg-primary-50 border-r-4 border-primary-600 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              } group flex items-center px-3 py-2 text-sm font-medium rounded-l-md transition-colors duration-200`}
            >
              <Icon
                className={`${
                  isActive(item.href) ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-500'
                } mr-3 h-5 w-5 transition-colors duration-200`}
              />
              {item.name}
            </Link>
          );
        })}
      </nav>

      {/* User info */}
      <div className="p-4 bg-gray-50 border-t border-gray-200">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="h-8 w-8 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {user?.nombre?.charAt(0).toUpperCase()}
              </span>
            </div>
          </div>
          <div className="ml-3 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">
              {user?.nombre}
            </p>
            <p className="text-xs text-gray-500 capitalize">
              {user?.rol?.replace('_', ' ')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Sidebar móvil */}
      <Transition.Root show={sidebarOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50 lg:hidden" onClose={setSidebarOpen}>
          <Transition.Child
            as={Fragment}
            enter="transition-opacity ease-linear duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-linear duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-900/80" />
          </Transition.Child>

          <div className="fixed inset-0 flex">
            <Transition.Child
              as={Fragment}
              enter="transition ease-in-out duration-300 transform"
              enterFrom="-translate-x-full"
              enterTo="translate-x-0"
              leave="transition ease-in-out duration-300 transform"
              leaveFrom="translate-x-0"
              leaveTo="-translate-x-full"
            >
              <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                <Transition.Child
                  as={Fragment}
                  enter="ease-in-out duration-300"
                  enterFrom="opacity-0"
                  enterTo="opacity-100"
                  leave="ease-in-out duration-300"
                  leaveFrom="opacity-100"
                  leaveTo="opacity-0"
                >
                  <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                    <button
                      type="button"
                      className="-m-2.5 p-2.5"
                      onClick={() => setSidebarOpen(false)}
                    >
                      <XMarkIcon className="h-6 w-6 text-white" />
                    </button>
                  </div>
                </Transition.Child>
                
                <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white shadow-xl">
                  <SidebarContent />
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition.Root>

      {/* Sidebar desktop */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white shadow-sm border-r border-gray-200">
          <SidebarContent />
        </div>
      </div>
    </>
  );
};

export default Sidebar;
