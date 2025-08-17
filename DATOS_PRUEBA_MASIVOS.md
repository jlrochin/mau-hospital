# 🎯 Datos de Prueba Masivos Generados

## 📊 Estadísticas Generadas

### **Datos Creados:**

- ✅ **105 Pacientes** (5 existentes + 100 nuevos)
- ✅ **109 Recetas** (9 existentes + 100 nuevas)
- ✅ **319 Detalles de Medicamentos** (múltiples medicamentos por receta)
- ✅ **60 Lotes de Medicamentos** (dispensaciones con lotes múltiples)
- ✅ **13 Usuarios** (admin + 8 nuevos usuarios de prueba)

### **Distribución por Estado de Recetas:**

- 🔸 **PENDIENTE**: 25 recetas
- 🔵 **VALIDADA**: 24 recetas
- 🟠 **PARCIALMENTE_SURTIDA**: 20 recetas
- 🟢 **SURTIDA**: 19 recetas
- 🔴 **CANCELADA**: 21 recetas

### **Distribución por Tipo:**

- 💊 **FARMACIA**: 65 recetas
- 🧪 **CMI**: 44 recetas

## 👥 Usuarios de Prueba Creados

### **Credenciales de Acceso:**

> **Password universal**: `123456` (para todos los usuarios de prueba)

| Usuario           | Nombre Completo | Rol              | Email                        |
| ----------------- | --------------- | ---------------- | ---------------------------- |
| `maria.gonzalez`  | María González  | ATENCION_USUARIO | maria.gonzalez@hospital.com  |
| `carlos.martinez` | Carlos Martínez | FARMACIA         | carlos.martinez@hospital.com |
| `ana.lopez`       | Ana López       | CMI              | ana.lopez@hospital.com       |
| `luis.rodriguez`  | Luis Rodríguez  | MEDICO           | luis.rodriguez@hospital.com  |
| `carmen.sanchez`  | Carmen Sánchez  | FARMACIA         | carmen.sanchez@hospital.com  |
| `francisco.perez` | Francisco Pérez | CMI              | francisco.perez@hospital.com |
| `isabel.garcia`   | Isabel García   | ATENCION_USUARIO | isabel.garcia@hospital.com   |
| `manuel.torres`   | Manuel Torres   | MEDICO           | manuel.torres@hospital.com   |

### **Usuario Administrador Existente:**

- **Usuario**: `admin`
- **Password**: `admin123`
- **Rol**: ADMIN (acceso completo)

## 🏥 Pacientes Generados

### **Características:**

- **Expedientes**: EXP001 a EXP100 (únicos)
- **Edades**: Entre 18 y 90 años
- **Nombres y Apellidos**: Datos realistas españoles
- **CURPs**: Generados con formato válido
- **Patologías**: 22 diferentes condiciones médicas
- **Códigos CIE10**: Correspondientes a las patologías

### **Ejemplos de Patologías Incluidas:**

- Hipertensión arterial (I10)
- Diabetes mellitus tipo 2 (E11)
- Insuficiencia cardíaca (I50)
- EPOC (J44)
- Artritis reumatoide (M06)
- Depresión mayor (F32)
- Y 16 más...

## 💊 Medicamentos y Recetas

### **20 Medicamentos Diferentes:**

- **MED001-MED020**: Medicamentos comunes hospitalarios
- **Formas farmacéuticas**: Tabletas, Cápsulas, Ampollas, Inhaladores, Frascos
- **Precios**: Rangos realistas ($0.50 - $50.00)

### **Ejemplos de Medicamentos:**

- Paracetamol 500mg
- Ibuprofeno 400mg
- Amoxicilina 500mg
- Losartán 50mg
- Metformina 850mg
- Insulina NPH 100 UI/ml
- Eritropoyetina 4000 UI
- Y 13 más...

### **Características de las Recetas:**

- **1-5 medicamentos** por receta
- **Servicios médicos**: 20 servicios diferentes
- **Prioridades**: URGENTE, ALTA, MEDIA, BAJA
- **Fechas**: Distribuidas en los últimos 30 días
- **Dispensaciones realistas**: Con lotes y fechas de caducidad

## 🧪 Casos de Prueba Disponibles

### **Para Testing de Estados:**

#### **🔸 Recetas Pendientes (25)**

- **Ideal para**: Probar módulo de validación
- **Usuario sugerido**: `maria.gonzalez` (ATENCION_USUARIO)

#### **🔵 Recetas Validadas (24)**

- **Ideal para**: Probar dispensación en farmacia/CMI
- **Usuarios sugeridos**: `carlos.martinez` (FARMACIA), `ana.lopez` (CMI)

#### **🟠 Recetas Parcialmente Surtidas (20)**

- **Ideal para**: Probar completar dispensaciones
- **Incluye**: Lotes múltiples y dispensaciones tradicionales

#### **🟢 Recetas Completadas (19)**

- **Ideal para**: Probar módulo de recetas completadas
- **Incluye**: Historial completo de dispensaciones

### **Para Testing de Roles:**

#### **👨‍⚕️ MEDICO/ATENCION_USUARIO:**

- Crear nuevas recetas
- Validar recetas pendientes
- Ver historial completo

#### **💊 FARMACIA:**

- Dispensar recetas de farmacia
- Ver solo recetas de farmacia completadas
- Gestionar lotes múltiples

#### **🧪 CMI:**

- Dispensar recetas de CMI
- Ver solo recetas de CMI completadas
- Gestionar mezclas especializadas

#### **👑 ADMIN:**

- Acceso completo a todos los módulos
- Ver todas las recetas y pacientes
- Gestión de usuarios

## 🚀 Casos de Uso para Testing

### **1. Flujo Completo de Receta:**

```
1. Login como MEDICO → Crear receta nueva
2. Login como ATENCION_USUARIO → Validar receta
3. Login como FARMACIA/CMI → Dispensar medicamentos
4. Verificar en módulo de recetas completadas
```

### **2. Dispensación con Lotes Múltiples:**

```
1. Buscar recetas parcialmente surtidas
2. Usar "Gestionar Lotes" en medicamentos
3. Agregar múltiples lotes hasta completar
4. Verificar historial detallado
```

### **3. Testing de Permisos:**

```
1. Login con diferentes roles
2. Verificar módulos disponibles en Dashboard
3. Confirmar filtros por tipo de receta
4. Validar restricciones de acceso
```

### **4. Búsquedas y Filtros:**

```
1. Buscar pacientes por expediente/nombre
2. Filtrar recetas por estado/tipo/fecha
3. Usar filtros en recetas completadas
4. Probar paginación con grandes volúmenes
```

### **5. Auditoría y Reportes:**

```
1. Ver historial detallado de dispensaciones
2. Verificar usuarios responsables
3. Comprobar fechas y timestamps
4. Validar trazabilidad de lotes
```

## 🎯 Escenarios de Prueba Específicos

### **Escenario 1: Hospital en Hora Pico**

- 25 recetas pendientes esperando validación
- 24 recetas validadas listas para dispensar
- Diferentes prioridades (URGENTE, ALTA, etc.)

### **Escenario 2: Farmacia Ocupada**

- 65 recetas de farmacia en diferentes estados
- Múltiples medicamentos por receta
- Lotes con diferentes fechas de caducidad

### **Escenario 3: CMI Especializado**

- 44 recetas de CMI para mezclas
- Medicamentos especializados (Eritropoyetina, Insulina)
- Dispensaciones complejas

### **Escenario 4: Auditoría Mensual**

- 109 recetas distribuidas en 30 días
- Historial completo de dispensaciones
- Múltiples usuarios involucrados

### **Escenario 5: Pacientes Complejos**

- 105 pacientes con diferentes patologías
- Edades desde 18 a 90 años
- Múltiples recetas por paciente

## 🔧 Comandos Útiles para Testing

### **Regenerar Datos:**

```bash
cd backend
python generate_test_data.py
```

### **Verificar Base de Datos:**

```bash
python manage.py shell
>>> from apps.patients.models import Paciente
>>> from apps.prescriptions.models import Receta
>>> print(f"Pacientes: {Paciente.objects.count()}")
>>> print(f"Recetas: {Receta.objects.count()}")
```

### **Limpiar Datos de Prueba:**

```bash
python manage.py shell
>>> from apps.patients.models import Paciente
>>> from apps.prescriptions.models import Receta
>>> # Solo eliminar datos de prueba
>>> Paciente.objects.filter(expediente__startswith='EXP').delete()
>>> Receta.objects.filter(paciente__expediente__startswith='EXP').delete()
```

## 📈 Métricas de Performance

Con este volumen de datos puedes probar:

- ✅ **Paginación** con listas grandes
- ✅ **Filtros** con múltiples criterios
- ✅ **Búsquedas** en texto completo
- ✅ **Ordenamiento** por diferentes campos
- ✅ **Carga de modales** con datos complejos
- ✅ **Actualización en tiempo real** con lotes
- ✅ **Navegación** entre múltiples páginas

---

**¡Ahora tienes un entorno completo con 100+ registros de cada tipo para hacer testing exhaustivo de todas las funcionalidades del sistema!** 🎉
