# Sistema de Auditoría del Sistema MAU

Este módulo proporciona un sistema completo de auditoría que captura automáticamente **solo las acciones importantes** del sistema, no la navegación rutinaria.

## Características

- **Captura selectiva**: Solo audita acciones importantes como login, logout, cambios de datos, etc.
- **Filtrado inteligente**: Excluye navegación rutinaria, consultas de dashboard, y recursos estáticos
- **Señales automáticas**: Captura cambios importantes en modelos Django (CREATE, UPDATE, DELETE)
- **Decoradores**: Para auditar acciones específicas en vistas
- **Utilidades**: Funciones helper para logging manual
- **API REST**: Endpoints para consultar y exportar logs de auditoría

## ¿Qué se audita automáticamente?

### ✅ SÍ se audita:

- **Autenticación**: Login, logout, registro de usuarios
- **Cambios de datos**: CREATE, UPDATE, DELETE en entidades principales
- **Acciones críticas**: Dispensación de recetas, validaciones, cambios de stock
- **Errores del sistema**: Excepciones y fallos
- **Reportes y exportaciones**: Generación y descarga de reportes
- **Cambios de configuración**: Modificaciones en usuarios y configuraciones
- **Acciones administrativas**: Cambios en el panel de administración

### ❌ NO se audita:

- **Navegación rutinaria**: Cambios de página, menús, navegación
- **Consultas de dashboard**: Estadísticas y métricas de visualización
- **Recursos estáticos**: Archivos CSS, JS, imágenes
- **Autocompletado**: Sugerencias de formularios
- **Peticiones de datos**: Listas, consultas de solo lectura
- **Campos menores**: Actualizaciones de timestamps, contadores de acceso

## Componentes

### 1. Middleware (`middleware.py`)

Captura automáticamente solo las peticiones HTTP importantes y crea registros de auditoría.

**Configuración automática**: Ya está incluido en `settings.py`

**Filtrado inteligente**: Solo audita acciones que cumplan criterios de importancia

### 2. Señales (`signals.py`)

Captura automáticamente cambios importantes en modelos Django.

**Configuración automática**: Se registran automáticamente al iniciar la app

**Filtrado por campos**: Solo audita cambios en campos importantes, no en campos menores

### 3. Decoradores (`decorators.py`)

Para auditar acciones específicas en vistas.

**Uso básico**:

```python
from apps.audit.decorators import audit_action

@audit_action('CREATE', 'PATIENT', 'Creación de paciente')
def create_patient(request):
    # código de la vista
    pass
```

**Decoradores especializados**:

```python
from apps.audit.decorators import audit_login, audit_delete, audit_critical

@audit_login()
def login_view(request):
    pass

@audit_delete()
def delete_patient(request, pk):
    pass

@audit_critical()
def critical_operation(request):
    pass
```

### 4. Utilidades (`utils.py`)

Funciones helper para logging manual.

**Logging básico**:

```python
from apps.audit.utils import log_action

log_action(
    action_type='CREATE',
    entity_type='PATIENT',
    description='Paciente creado exitosamente',
    user=request.user,
    entity_id=patient.id,
    module='PATIENTS'
)
```

**Logging de usuario**:

```python
from apps.audit.utils import log_user_action

log_user_action(
    user=request.user,
    action_type='LOGIN',
    description='Usuario inició sesión'
)
```

**Logging de modelo**:

```python
from apps.audit.utils import log_model_action

log_model_action(
    action_type='CREATE',
    model_instance=patient,
    description='Paciente creado',
    user=request.user
)
```

**Logging de errores**:

```python
from apps.audit.utils import log_error

try:
    # código que puede fallar
    pass
except Exception as e:
    log_error(
        error=e,
        context='Vista de pacientes',
        user=request.user
    )
```

**Medición de rendimiento**:

```python
from apps.audit.utils import AuditTimer

with AuditTimer('Consulta de pacientes', user=request.user) as timer:
    patients = Patient.objects.all()
    # El tiempo se mide y registra automáticamente
```

### 5. API REST

Endpoints disponibles:

- `GET /api/audit/` - Lista de registros de auditoría
- `GET /api/audit/stats/` - Estadísticas generales
- `GET /api/audit/summary/` - Resumen diario/semanal
- `GET /api/audit/export/` - Exportar registros

**Filtros disponibles**:

- `action_type`: Tipo de acción (CREATE, UPDATE, DELETE, etc.)
- `entity_type`: Tipo de entidad (PATIENT, PRESCRIPTION, etc.)
- `user`: Usuario que realizó la acción
- `date_from` / `date_to`: Rango de fechas
- `module`: Módulo del sistema

## Configuración

### 1. Agregar a INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... otras apps
    'apps.audit',
]
```

### 2. Agregar middleware

```python
MIDDLEWARE = [
    # ... otros middlewares
    'apps.audit.middleware.AuditMiddleware',
]
```

### 3. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Generación de Datos de Ejemplo

Para generar datos de auditoría de ejemplo (solo acciones importantes):

```bash
python manage.py generate_audit_data --count 50 --days 30
```

**Parámetros**:

- `--count`: Número de registros a generar (default: 50)
- `--days`: Días hacia atrás para generar datos (default: 30)

**Nota**: Solo genera acciones importantes, no navegación rutinaria

## Campos del Modelo SystemMovement

- **action_type**: Tipo de acción (CREATE, UPDATE, DELETE, LOGIN, etc.)
- **entity_type**: Tipo de entidad afectada
- **entity_id**: ID de la entidad
- **object_id**: ID del objeto específico
- **description**: Descripción de la acción
- **user**: Usuario que realizó la acción
- **ip_address**: Dirección IP del usuario
- **user_agent**: User agent del navegador
- **session_id**: ID de la sesión
- **module**: Módulo del sistema
- **function_name**: Nombre de la función
- **timestamp**: Fecha y hora de la acción
- **execution_time**: Tiempo de ejecución en milisegundos
- **is_successful**: Si la acción fue exitosa
- **priority**: Prioridad (LOW, MEDIUM, HIGH, CRITICAL)
- **error_message**: Mensaje de error si falló
- **tags**: Metadatos adicionales en formato JSON

## Ejemplos de Uso

### En una vista de creación de paciente:

```python
from apps.audit.decorators import audit_action

@audit_action('CREATE', 'PATIENT', 'Creación de paciente')
def create_patient(request):
    # lógica de creación
    patient = Patient.objects.create(...)

    # El registro de auditoría se crea automáticamente
    return Response({'id': patient.id})
```

### En una vista con logging manual:

```python
from apps.audit.utils import log_action, AuditTimer

def complex_operation(request):
    with AuditTimer('Operación compleja', user=request.user) as timer:
        # código de la operación
        result = perform_complex_operation()

        # Logging adicional
        log_action(
            action_type='COMPLEX_OP',
            entity_type='SYSTEM',
            description='Operación compleja completada',
            user=request.user,
            tags={'result': result}
        )

        return Response({'result': result})
```

### En un modelo con señales automáticas:

```python
# Las señales se registran automáticamente para modelos comunes
# Solo audita cambios importantes, no modificaciones menores
```

## Personalización del Filtrado

### Modificar qué se audita en el middleware:

Edita el método `should_audit_request` en `middleware.py`:

```python
def should_audit_request(self, request, response):
    # Agregar o quitar rutas según tus necesidades
    excluded_paths = [
        '/api/reports/dashboard/',
        '/api/recetas/estadisticas/',
        # ... más rutas a excluir
    ]

    important_actions = [
        '/api/auth/login/',
        '/api/patients/create/',
        # ... más acciones importantes
    ]

    # Tu lógica personalizada aquí
```

### Modificar qué campos se auditan en modelos:

Edita la función `create_model_audit_signal` en `signals.py`:

```python
# Definir campos menores que no requieren auditoría
minor_fields = {
    'last_modified', 'updated_at', 'modified_at',
    'last_accessed', 'access_count', 'view_count',
    'cache_timestamp', 'sync_status',
    # ... tus campos menores
}
```

## Monitoreo y Mantenimiento

### Limpieza de logs antiguos

Para mantener la base de datos optimizada, considera implementar un comando de limpieza:

```python
# En un comando de gestión
from datetime import timedelta
from django.utils import timezone

# Eliminar logs más antiguos de 1 año
cutoff_date = timezone.now() - timedelta(days=365)
SystemMovement.objects.filter(timestamp__lt=cutoff_date).delete()
```

### Estadísticas de rendimiento

El sistema registra automáticamente:

- Tiempo de ejecución de peticiones importantes
- Tiempo de ejecución de operaciones decoradas
- Errores y excepciones
- Acciones de usuarios
- Cambios importantes en modelos

## Troubleshooting

### Error: "Model class doesn't declare an explicit app_label"

Asegúrate de que la app esté en `INSTALLED_APPS` y que el modelo tenga `app_label` definido.

### Error: "Field doesn't exist"

Verifica que todos los campos referenciados en el serializer existan en el modelo.

### Logs no se están creando

1. Verifica que el middleware esté en `MIDDLEWARE`
2. Verifica que la app esté en `INSTALLED_APPS`
3. Revisa los logs de Django para errores
4. Verifica que las migraciones se hayan ejecutado

### Se están creando demasiados logs

1. Verifica la configuración de filtrado en `should_audit_request`
2. Ajusta las rutas excluidas según tus necesidades
3. Revisa las señales de modelos para campos menores

## Ventajas del Sistema Selectivo

1. **Base de datos más limpia**: Solo logs relevantes
2. **Mejor rendimiento**: Menos registros que procesar
3. **Análisis más útil**: Enfoque en acciones importantes
4. **Menor ruido**: No se pierden en navegación rutinaria
5. **Compliance**: Cumple con requisitos de auditoría sin sobrecarga
