import React from 'react';
import { ChartBarIcon } from '@heroicons/react/24/outline';

const Reports = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reportes y Análisis</h1>
          <p className="mt-2 text-sm text-gray-700">
            Análisis detallado y reportes del proceso de reclutamiento
          </p>
        </div>
      </div>

      {/* Coming Soon */}
      <div className="text-center py-12">
        <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-lg font-medium text-gray-900">Próximamente</h3>
        <p className="mt-1 text-sm text-gray-500">
          Los reportes detallados estarán disponibles pronto.
        </p>
      </div>
    </div>
  );
};

export default Reports;
