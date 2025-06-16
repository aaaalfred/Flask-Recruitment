import { useState, useEffect } from 'react';

/**
 * Hook personalizado para implementar debounce
 * @param {*} value - Valor a debouncear 
 * @param {number} delay - Delay en milisegundos (default: 500ms)
 * @returns {*} - Valor debounceado
 */
const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Crear un timeout que actualiza el valor debounceado después del delay
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cleanup: cancelar el timeout si el valor cambia antes del delay
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

export default useDebounce;
