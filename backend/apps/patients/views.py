from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Paciente, CIE10Mexico
from .serializers import (
    PacienteSerializer, PacienteBusquedaSerializer,
    PacienteCreateSerializer, PacienteUpdateSerializer,
    CIE10MexicoSerializer, CIE10MexicoBusquedaSerializer
)

class PacienteListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear pacientes"""
    
    queryset = Paciente.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genero', 'tipo_sangre', 'institucion_seguro']
    search_fields = ['expediente', 'nombre', 'apellido_paterno', 'apellido_materno', 'curp']
    ordering_fields = ['expediente', 'apellido_paterno', 'fecha_nacimiento', 'created_at']
    ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PacienteCreateSerializer
        elif self.request.GET.get('simple') == 'true':
            return PacienteBusquedaSerializer
        return PacienteSerializer
    
    def get_queryset(self):
        """Filtros adicionales para búsqueda"""
        queryset = super().get_queryset()
        
        # Búsqueda por expediente específico
        expediente = self.request.query_params.get('expediente')
        if expediente:
            queryset = queryset.filter(expediente__icontains=expediente)
        
        # Búsqueda por CURP específica
        curp = self.request.query_params.get('curp')
        if curp:
            queryset = queryset.filter(curp__icontains=curp)
        
        # Búsqueda por rango de edad
        edad_min = self.request.query_params.get('edad_min')
        edad_max = self.request.query_params.get('edad_max')
        if edad_min or edad_max:
            from datetime import date, timedelta
            today = date.today()
            
            if edad_min:
                fecha_max = today - timedelta(days=int(edad_min) * 365)
                queryset = queryset.filter(fecha_nacimiento__lte=fecha_max)
            
            if edad_max:
                fecha_min = today - timedelta(days=(int(edad_max) + 1) * 365)
                queryset = queryset.filter(fecha_nacimiento__gte=fecha_min)
        
        return queryset
    
    def perform_create(self, serializer):
        """Solo usuarios con rol 'ATENCION_USUARIO' pueden crear pacientes"""
        if not self.request.user.can_create_patients():
            raise PermissionError("No tiene permisos para crear pacientes")
        
        serializer.save()

class PacienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar y eliminar pacientes específicos"""
    
    queryset = Paciente.objects.all()
    lookup_field = 'expediente'
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PacienteUpdateSerializer
        return PacienteSerializer
    
    def perform_update(self, serializer):
        """Solo usuarios con rol 'ATENCION_USUARIO' pueden editar pacientes"""
        if not self.request.user.can_edit_patients():
            raise PermissionError("No tiene permisos para editar pacientes")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Eliminación lógica (marcar como inactivo)"""
        if not self.request.user.can_edit_patients():
            raise PermissionError("No tiene permisos para eliminar pacientes")
        
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_paciente(request):
    """Endpoint especializado para búsqueda rápida de pacientes"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({
            'error': 'Parámetro de búsqueda requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Buscar por expediente, CURP o nombre
    pacientes = Paciente.objects.filter(
        Q(expediente__icontains=query) |
        Q(curp__icontains=query) |
        Q(nombre__icontains=query) |
        Q(apellido_paterno__icontains=query) |
        Q(apellido_materno__icontains=query),
        is_active=True
    ).order_by('apellido_paterno', 'apellido_materno', 'nombre')[:10]
    
    serializer = PacienteBusquedaSerializer(pacientes, many=True)
    
    return Response({
        'results': serializer.data,
        'total': pacientes.count()
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verificar_duplicados(request):
    """Endpoint para verificar si existen duplicados antes de crear un paciente"""
    expediente = request.GET.get('expediente', '').strip().upper()
    curp = request.GET.get('curp', '').strip().upper()
    
    if not expediente and not curp:
        return Response({
            'error': 'Se requiere expediente o CURP para verificar'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    duplicados = []
    
    if expediente:
        paciente_expediente = Paciente.objects.filter(expediente=expediente).first()
        if paciente_expediente:
            duplicados.append({
                'tipo': 'expediente',
                'campo': 'expediente',
                'valor': expediente,
                'paciente': PacienteBusquedaSerializer(paciente_expediente).data
            })
    
    if curp:
        paciente_curp = Paciente.objects.filter(curp=curp).first()
        if paciente_curp:
            duplicados.append({
                'tipo': 'curp',
                'campo': 'curp',
                'valor': curp,
                'paciente': PacienteBusquedaSerializer(paciente_curp).data
            })
    
    return Response({
        'duplicados_encontrados': len(duplicados) > 0,
        'duplicados': duplicados
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paciente_historial(request, expediente):
    """Endpoint para obtener el historial completo de un paciente"""
    try:
        paciente = Paciente.objects.get(expediente=expediente)
    except Paciente.DoesNotExist:
        return Response({
            'error': 'Paciente no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Información del paciente
    paciente_data = PacienteSerializer(paciente).data
    
    # Historial de recetas
    from apps.prescriptions.serializers import RecetaListSerializer
    recetas = paciente.recetas.all().order_by('-fecha_creacion')
    recetas_data = RecetaListSerializer(recetas, many=True).data
    
    return Response({
        'paciente': paciente_data,
        'recetas': recetas_data,
        'total_recetas': recetas.count(),
        'recetas_pendientes': recetas.filter(estado='PENDIENTE').count(),
        'recetas_validadas': recetas.filter(estado='VALIDADA').count(),
        'recetas_surtidas': recetas.filter(estado='SURTIDA').count()
    })


class CIE10MexicoListView(generics.ListAPIView):
    """Vista para listar códigos CIE-10 México"""
    
    queryset = CIE10Mexico.objects.filter(activo=True)
    serializer_class = CIE10MexicoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['capitulo', 'categoria', 'tipo', 'genero_aplicable']
    search_fields = ['codigo', 'descripcion', 'descripcion_corta']
    ordering_fields = ['codigo', 'capitulo', 'categoria']
    ordering = ['codigo']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_cie10(request):
    """Endpoint especializado para búsqueda rápida de códigos CIE-10"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({
            'error': 'Parámetro de búsqueda requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Buscar por código o descripción
    codigos = CIE10Mexico.objects.filter(
        Q(codigo__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(descripcion_corta__icontains=query),
        activo=True
    ).order_by('codigo')[:20]
    
    serializer = CIE10MexicoBusquedaSerializer(codigos, many=True)
    
    return Response({
        'results': serializer.data,
        'total': codigos.count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cie10_para_paciente(request, expediente):
    """Endpoint para obtener códigos CIE-10 aplicables a un paciente específico"""
    try:
        paciente = Paciente.objects.get(expediente=expediente)
    except Paciente.DoesNotExist:
        return Response({
            'error': 'Paciente no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Filtrar códigos aplicables para el paciente
    codigos_aplicables = []
    todos_codigos = CIE10Mexico.objects.filter(activo=True)
    
    for codigo in todos_codigos:
        if codigo.is_aplicable_for_patient(paciente):
            codigos_aplicables.append(codigo)
    
    serializer = CIE10MexicoBusquedaSerializer(codigos_aplicables, many=True)
    
    return Response({
        'paciente': PacienteBusquedaSerializer(paciente).data,
        'codigos_aplicables': serializer.data,
        'total': len(codigos_aplicables)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estadisticas_cie10(request):
    """Endpoint para obtener estadísticas del catálogo CIE-10"""
    total_codigos = CIE10Mexico.objects.filter(activo=True).count()
    
    # Estadísticas por capítulo
    capitulos = CIE10Mexico.objects.filter(activo=True).values('capitulo').distinct()
    stats_capitulos = []
    
    for cap in capitulos:
        capitulo = cap['capitulo']
        count = CIE10Mexico.objects.filter(capitulo=capitulo, activo=True).count()
        stats_capitulos.append({
            'capitulo': capitulo,
            'total_codigos': count
        })
    
    # Estadísticas por tipo
    tipos = CIE10Mexico.objects.filter(activo=True).values('tipo').distinct()
    stats_tipos = []
    
    for tipo in tipos:
        tipo_codigo = tipo['tipo']
        count = CIE10Mexico.objects.filter(tipo=tipo_codigo, activo=True).count()
        stats_tipos.append({
            'tipo': tipo_codigo,
            'total_codigos': count
        })
    
    return Response({
        'total_codigos': total_codigos,
        'estadisticas_capitulos': sorted(stats_capitulos, key=lambda x: x['capitulo']),
        'estadisticas_tipos': stats_tipos,
        'codigos_mortalidad': CIE10Mexico.objects.filter(es_mortalidad=True, activo=True).count(),
        'codigos_morbilidad': CIE10Mexico.objects.filter(es_morbilidad=True, activo=True).count()
    })
