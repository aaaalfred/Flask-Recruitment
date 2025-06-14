# 🧪 GUÍA DE PRUEBAS DE VALIDACIONES DE FECHAS

## 📋 Casos de Prueba

### ✅ **Casos que DEBEN Pasar:**
1. **Fecha envío futura + Fecha límite posterior**
   - Envío: Mañana 10:00 AM
   - Límite: Pasado mañana 5:00 PM
   - ✅ Resultado esperado: Se guarda correctamente

2. **Solo fecha límite futura (sin fecha envío)**
   - Envío: (vacío)
   - Límite: Próxima semana
   - ✅ Resultado esperado: Se guarda correctamente

### ❌ **Casos que DEBEN Fallar:**

3. **Fecha envío en el pasado**
   - Envío: Ayer
   - Error esperado: "La fecha debe ser posterior al día de hoy"

4. **Fecha límite en el pasado**
   - Límite: Ayer
   - Error esperado: "La fecha debe ser posterior al día de hoy"

5. **Fecha límite anterior a fecha envío**
   - Envío: Próxima semana
   - Límite: Mañana
   - Error esperado: "La fecha límite debe ser posterior a la fecha de envío de candidatos"

6. **Fechas iguales**
   - Envío: Mañana 10:00 AM
   - Límite: Mañana 10:00 AM
   - Error esperado: "La fecha límite debe ser posterior a la fecha de envío de candidatos"

## 🎯 **Comportamiento Dinámico Esperado:**

- Al seleccionar fecha de envío, el mínimo de fecha límite debe actualizarse
- Los mensajes de ayuda deben cambiar dinámicamente
- La validación debe ejecutarse en tiempo real
- Los calendarios deben prevenir selección de fechas inválidas

## 🔧 **Elementos a Verificar:**

1. **Campo Fecha Envío:**
   - `min` attribute = hoy
   - Mensaje: "Fecha cuando se envían candidatos (debe ser futura)"

2. **Campo Fecha Límite:**
   - `min` attribute = fecha envío OR hoy (dinámico)
   - Mensaje cambia según si hay fecha envío seleccionada

3. **Errores de Validación:**
   - Aparecen en rojo debajo del campo
   - Textos específicos para cada tipo de error
   - Previenen el envío del formulario

## 🚀 **Configuraciones Automáticas a Verificar:**

- Estado: Siempre "🆕 Creada"
- Reclutador Líder: Siempre "👑 Fernanda Moreno"
- Campos no editables mostrados en gris
