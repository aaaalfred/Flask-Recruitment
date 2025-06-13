import React from 'react';
import { UsersIcon } from '@heroicons/react/24/outline';

const Users = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
          <p className="mt-2 text-sm text-gray-700">
            Administra los usuarios del sistema y sus permisos
          </p>
        </div>
      </div>

      {/* Coming Soon */}
      <div className="text-center py-12">
        <UsersIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-lg font-medium text-gray-900">Próximamente</h3>
        <p className="mt-1 text-sm text-gray-500">
          La gestión de usuarios estará disponible pronto.
        </p>
      </div>
    </div>
  );
};

export default Users;
