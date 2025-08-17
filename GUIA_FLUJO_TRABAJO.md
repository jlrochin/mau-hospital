# 🏥 **GUÍA DEL FLUJO DE TRABAJO - Sistema de Gestión de Recetas**

## 📋 **Datos de Ejemplo Creados**

### **👥 Pacientes en el Sistema**

- **EXP001** - Juan Gómez López (Hipertensión Arterial)
- **EXP002** - María Rodríguez Sánchez (Diabetes Mellitus Tipo 2)
- **EXP003** - Carlos Pérez Ruiz (Cáncer de Pulmón)
- **EXP004** - Ana Hernández Álvarez (Artritis Reumatoide)
- **EXP005** - Jorge Torres López (Insuficiencia Renal Crónica)

### **📜 Recetas por Estado**

- **🟡 PENDIENTES**: 5 recetas (4 Farmacia, 1 CMI)
- **🟢 VALIDADAS**: 4 recetas (2 Farmacia, 2 CMI)
- **📊 Total**: 9 recetas en el sistema

---

## 🔄 **FLUJO DE TRABAJO COMPLETO**

### **1️⃣ INICIO DE SESIÓN**

**URL**: http://localhost:3000

**Credenciales de Prueba**:

```
👨‍⚕️ Atención al Usuario:
   Usuario: atencion01
   Contraseña: password123

💊 Farmacia:
   Usuario: farmacia01
   Contraseña: password123

🏥 CMI (Centro de Mezclas):
   Usuario: cmi01
   Contraseña: password123

👨‍💼 Administrador:
   Usuario: admin
   Contraseña: admin123
```

---

### **2️⃣ MÓDULO: ATENCIÓN AL USUARIO**

_Responsabilidad: Gestión de pacientes y validación de recetas_

#### **A) Gestión de Pacientes**

1. **Buscar Pacientes**:

   - Ve a "Buscar Paciente"
   - Prueba buscar por expediente: `EXP001`
   - O por nombre: `Juan`

2. **Ver Detalles del Paciente**:
   - Información completa del paciente
   - Historial de recetas

#### **B) Validación de Recetas**

1. **Cola de Validación**:

   - Ve a "Cola de Validación"
   - Verás **5 recetas PENDIENTES** esperando validación
   - Cada receta muestra: paciente, servicio, tipo, medicamentos

2. **Proceso de Validación**:
   - Selecciona una receta PENDIENTE
   - Revisa los medicamentos y dosis
   - Marca como "VALIDADA" para enviar a dispensación
   - O rechaza si hay errores

---

### **3️⃣ MÓDULO: FARMACIA**

_Responsabilidad: Dispensación de medicamentos orales y tabletas_

#### **A) Cola de Dispensación**

1. **Acceso**:

   - Inicia sesión como `farmacia01`
   - Ve a "Cola de Dispensación"

2. **Recetas Disponibles**:

   - Verás **2 recetas VALIDADAS** tipo FARMACIA
   - Receta #6: Jorge Torres (Eritropoyetina, Furosemida, Carbonato de Calcio)
   - Receta #7: Juan Gómez (Atorvastatina, Aspirina)

3. **Proceso de Dispensación**:
   - Selecciona una receta
   - Agrega información de lote y fecha de caducidad
   - Marca cantidad surtida
   - Cambia estado a "SURTIDA"

---

### **4️⃣ MÓDULO: CMI (CENTRO DE MEZCLAS)**

_Responsabilidad: Preparación de mezclas intravenosas y terapias especializadas_

#### **A) Cola de Dispensación CMI**

1. **Acceso**:

   - Inicia sesión como `cmi01`
   - Ve a "Cola de Dispensación CMI"

2. **Recetas Disponibles**:

   - Verás **2 recetas VALIDADAS** tipo CMI
   - Receta #8: María Rodríguez (Insulina, Soluciones)
   - Receta #9: Ana Hernández (Adalimumab, Agua estéril)

3. **Proceso de Preparación**:
   - Selecciona una receta
   - Prepara la mezcla según protocolo
   - Agrega información de lote y caducidad
   - Marca estado como "SURTIDA"

---

## 🎯 **CASOS DE USO PARA PROBAR**

### **Escenario 1: Flujo Completo - Validación de Receta**

1. Entra como `atencion01`
2. Ve a "Cola de Validación"
3. Selecciona la receta de "Juan Gómez" (Losartán e Hidroclorotiazida)
4. Valida la receta
5. Cierra sesión y entra como `farmacia01`
6. Ve a "Cola de Dispensación"
7. Procesa la receta recién validada

### **Escenario 2: Búsqueda de Pacientes**

1. Entra como cualquier usuario
2. Ve a "Buscar Paciente"
3. Busca por expediente: `EXP003` (Carlos Pérez)
4. Revisa su información y historial de recetas

### **Escenario 3: Dispensación CMI**

1. Entra como `cmi01`
2. Ve a "Cola de Dispensación CMI"
3. Selecciona la receta de quimioterapia para María Rodríguez
4. Prepara la mezcla de Insulina
5. Marca como dispensada

### **Escenario 4: Gestión Administrativa**

1. Entra como `admin`
2. Accede al panel de administración: http://localhost:8000/admin/
3. Revisa usuarios, pacientes y recetas
4. Modifica estados o información según sea necesario

---

## 📊 **MÉTRICAS Y ESTADÍSTICAS**

El sistema muestra en tiempo real:

- Total de recetas por estado
- Recetas pendientes por módulo
- Tiempo promedio de procesamiento
- Histórico de dispensaciones

---

## 🔧 **URLS DE ACCESO DIRECTO**

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000/api/
- **Panel Admin**: http://localhost:8000/admin/
- **Login API**: http://localhost:8000/api/auth/login/
- **Pacientes API**: http://localhost:8000/api/pacientes/
- **Recetas API**: http://localhost:8000/api/recetas/

---

## ⚠️ **NOTAS IMPORTANTES**

1. **Permisos por Rol**:

   - Solo "Atención al Usuario" puede crear/editar pacientes
   - Solo "Atención al Usuario" puede validar recetas
   - "Farmacia" y "CMI" solo pueden dispensar sus tipos de recetas

2. **Estados de Recetas**:

   - `PENDIENTE` → Recién creada, esperando validación
   - `VALIDADA` → Aprobada, lista para dispensación
   - `SURTIDA` → Medicamentos entregados
   - `CANCELADA` → Receta cancelada

3. **Tipos de Recetas**:

   - `FARMACIA` → Medicamentos orales, tabletas, jarabes
   - `CMI` → Mezclas intravenosas, quimioterapias, terapias especializadas

4. **Expediente como Clave Maestra**:
   - El expediente conecta al paciente con todas sus recetas
   - Es único e inmutable en el sistema

---

## 🚀 **¡SISTEMA LISTO PARA USO!**

Todo el flujo de trabajo está configurado con datos reales de ejemplo. Puedes seguir cualquiera de los escenarios arriba para ver el sistema en funcionamiento completo.
