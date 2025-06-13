import React from 'react';
import { CalendarDaysIcon } from '@heroicons/react/24/outline';

const Interviews = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Gestión de Entrevistas</h1>
          <p className="mt-2 text-sm text-gray-700">
            Programa y gestiona las entrevistas con candidatos
          </p>
        </div>
      </div>

      {/* Coming Soon */}
      <div className="text-center py-12">
        <CalendarDaysIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-lg font-medium text-gray-900">Próximamente</h3>
        <p className="mt-1 text-sm text-gray-500">
          La gestión de entrevistas estará disponible pronto.
        </p>
      </div>
    </div>
  );
};

export default Interviews;
