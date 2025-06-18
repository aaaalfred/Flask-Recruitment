// ===================================
// SCRIPT DE DIAGNÓSTICO PARA CONSOLA DEL NAVEGADOR
// ===================================
// Copiar y pegar este código en la consola del navegador (F12)
// cuando estés en la página del dashboard

console.log('🚀 INICIANDO DIAGNÓSTICO DEL DASHBOARD');

// 1. Verificar configuración de la API
const API_BASE_URL = 'http://localhost:5000/api';
console.log('🔗 API Base URL:', API_BASE_URL);

// 2. Verificar token en localStorage
const token = localStorage.getItem('authToken');
const userInfo = localStorage.getItem('userInfo');

console.log('🔐 Token en localStorage:', token ? `${token.substr(0, 50)}...` : 'NO ENCONTRADO');
console.log('👤 User info:', userInfo ? JSON.parse(userInfo) : 'NO ENCONTRADO');

if (!token) {
    console.error('❌ PROBLEMA: No hay token de autenticación guardado');
    console.log('💡 SOLUCIÓN: Hacer login nuevamente');
} else {
    console.log('✅ Token encontrado, procediendo con las pruebas...');
}

// 3. Test de conectividad básica
async function testHealth() {
    try {
        console.log('🔍 Probando conectividad básica...');
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('✅ Health check exitoso:', data);
        return true;
    } catch (error) {
        console.error('❌ Error en health check:', error);
        console.log('💡 SOLUCIÓN: Verificar que el backend esté corriendo en localhost:5000');
        return false;
    }
}

// 4. Test del endpoint de dashboard específico
async function testDashboard() {
    if (!token) {
        console.error('❌ No se puede probar dashboard sin token');
        return;
    }
    
    try {
        console.log('🔍 Probando endpoint del dashboard...');
        
        const response = await fetch(`${API_BASE_URL}/reports/dashboard`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        console.log('📡 Response status:', response.status);
        console.log('📡 Response headers:', Object.fromEntries(response.headers.entries()));
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Dashboard data recibida exitosamente:');
            console.table({
                'Total Vacantes': data.total_vacantes,
                'Vacantes Abiertas': data.vacantes_abiertas,
                'Total Candidatos': data.total_candidatos,
                'Entrevistas Pendientes': data.entrevistas_pendientes,
                'Usuario': data.usuario_nombre,
                'Rol': data.tipo_usuario
            });
            
            console.log('📊 Datos completos:', data);
            return data;
        } else {
            const errorData = await response.text();
            console.error('❌ Error en dashboard:', response.status, errorData);
            
            if (response.status === 401) {
                console.log('💡 SOLUCIÓN: Token inválido, hacer login nuevamente');
            } else if (response.status === 500) {
                console.log('💡 SOLUCIÓN: Error del servidor, revisar logs del backend');
            }
        }
    } catch (error) {
        console.error('❌ Error de red o CORS:', error);
        console.log('💡 SOLUCIÓN: Verificar CORS y conectividad');
    }
}

// 5. Test del servicio reportService directamente
async function testReportService() {
    // Solo funciona si estamos en la página de React
    if (typeof window.reportService !== 'undefined') {
        try {
            console.log('🔍 Probando reportService directamente...');
            const data = await window.reportService.getDashboardStats();
            console.log('✅ reportService funciona:', data);
        } catch (error) {
            console.error('❌ Error en reportService:', error);
        }
    } else {
        console.log('ℹ️ reportService no disponible (normal si no estás en React)');
    }
}

// 6. Verificar estado de React y componentes
function checkReactState() {
    // Solo funciona en la página de React
    if (typeof React !== 'undefined') {
        console.log('✅ React está cargado');
        
        // Buscar el componente Dashboard en el DOM
        const dashboardElement = document.querySelector('[class*="dashboard"], [class*="Dashboard"]');
        if (dashboardElement) {
            console.log('✅ Elemento Dashboard encontrado en DOM');
        } else {
            console.log('⚠️ Elemento Dashboard no encontrado en DOM');
        }
    } else {
        console.log('ℹ️ React no detectado (normal si no estás en la página React)');
    }
}

// 7. Ejecutar todas las pruebas
async function runAllTests() {
    console.log('\n🧪 EJECUTANDO TODAS LAS PRUEBAS...\n');
    
    await testHealth();
    console.log('\n' + '='.repeat(50) + '\n');
    
    await testDashboard();
    console.log('\n' + '='.repeat(50) + '\n');
    
    await testReportService();
    console.log('\n' + '='.repeat(50) + '\n');
    
    checkReactState();
    console.log('\n' + '='.repeat(50) + '\n');
    
    console.log('🏁 DIAGNÓSTICO COMPLETADO');
    console.log('💡 Si todos los tests pasan pero el dashboard muestra 0:');
    console.log('   1. Revisar que el estado del componente React se actualice');
    console.log('   2. Verificar errores en la consola de React');
    console.log('   3. Comprobar que el useEffect se ejecute correctamente');
}

// Ejecutar automáticamente
runAllTests();

// También exportar las funciones para uso manual
window.dashboardDiagnostic = {
    testHealth,
    testDashboard,
    testReportService,
    checkReactState,
    runAllTests
};

console.log('📋 Funciones disponibles: window.dashboardDiagnostic');
