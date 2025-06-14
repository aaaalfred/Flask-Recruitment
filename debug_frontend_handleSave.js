// Función handleSave mejorada con debugging detallado
// Reemplazar la función handleSave en Users.js líneas 120-160

const handleSave = async (e) => {
  e.preventDefault();
  
  console.log('🔧 DEBUG: Iniciando creación de usuario');
  console.log('FormData:', formData);
  console.log('EditingUser:', editingUser);
  
  try {
    const token = localStorage.getItem('token');
    console.log('Token:', token ? `${token.substring(0, 50)}...` : 'NO TOKEN');
    
    const url = editingUser 
      ? `http://localhost:5000/api/usuarios/${editingUser.id}`
      : 'http://localhost:5000/api/usuarios';
    
    const method = editingUser ? 'PUT' : 'POST';
    
    // Para edición, no enviamos password si está vacío
    const dataToSend = { ...formData };
    if (editingUser && !formData.password) {
      delete dataToSend.password;
    }

    console.log('🌐 Request details:');
    console.log('  URL:', url);
    console.log('  Method:', method);
    console.log('  Headers:', {
      'Authorization': `Bearer ${token ? token.substring(0, 30) + '...' : 'NO TOKEN'}`,
      'Content-Type': 'application/json'
    });
    console.log('  Body:', JSON.stringify(dataToSend, null, 2));

    const response = await fetch(url, {
      method,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataToSend)
    });

    console.log('📡 Response details:');
    console.log('  Status:', response.status);
    console.log('  StatusText:', response.statusText);
    console.log('  Headers:', Object.fromEntries(response.headers.entries()));

    if (response.ok) {
      const result = await response.json();
      console.log('✅ Success response:', result);
      toast.success(editingUser ? 'Usuario actualizado exitosamente' : 'Usuario creado exitosamente');
      resetForm();
      fetchUsuarios();
    } else {
      console.log('❌ Error response - Status:', response.status);
      
      // Intentar obtener el error como JSON
      try {
        const error = await response.json();
        console.log('❌ Error JSON:', error);
        toast.error(error.message || 'Error al guardar usuario');
      } catch (jsonError) {
        // Si no es JSON, obtener como texto
        const errorText = await response.text();
        console.log('❌ Error Text:', errorText);
        toast.error(`Error ${response.status}: ${errorText}`);
      }
    }
  } catch (error) {
    console.error('❌ Exception caught:', error);
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    });
    toast.error(`Error de conexión: ${error.message}`);
  }
};

// INSTRUCCIONES DE USO:
// 1. Abrir DevTools (F12) en el navegador
// 2. Ir a la pestaña Console
// 3. Intentar crear un usuario
// 4. Revisar todos los logs que aparecen con 🔧, 🌐, 📡, ✅, ❌
// 5. Copiar y pegar TODOS los logs aquí para analizarlos
