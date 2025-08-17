from rest_framework import serializers
from .models import Paciente, CIE10Mexico

class PacienteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Paciente"""
    
    nombre_completo = serializers.SerializerMethodField()
    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = [
            'expediente', 'nombre', 'apellido_paterno', 'apellido_materno',
            'nombre_completo', 'curp', 'fecha_nacimiento', 'edad', 'genero',
            'patologia', 'cie10', 'fecha_diagnostico', 'tipo_sangre', 'alergias',
            'telefono', 'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'numero_seguro_social',
            'institucion_seguro', 'is_active', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]
        read_only_fields = [
            'nombre_completo', 'edad', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]
    
    def get_nombre_completo(self, obj):
        return obj.get_nombre_completo()
    
    def get_edad(self, obj):
        return obj.get_edad()
    
    def validate_expediente(self, value):
        """Validación personalizada para expediente"""
        if not value:
            raise serializers.ValidationError("El expediente es requerido")
        
        # Convertir a mayúsculas
        value = value.upper()
        
        # Verificar si ya existe (solo en creación)
        if not self.instance and Paciente.objects.filter(expediente=value).exists():
            raise serializers.ValidationError(
                f"Ya existe un paciente con el expediente {value}"
            )
        
        return value
    
    def validate_curp(self, value):
        """Validación personalizada para CURP"""
        if not value:
            raise serializers.ValidationError("La CURP es requerida")
        
        # Convertir a mayúsculas
        value = value.upper()
        
        # Verificar si ya existe (solo en creación o si cambió)
        existing_patient = Paciente.objects.filter(curp=value).first()
        if existing_patient and existing_patient != self.instance:
            raise serializers.ValidationError(
                f"Ya existe un paciente con la CURP {value} (Expediente: {existing_patient.expediente})"
            )
        
        return value

class PacienteBusquedaSerializer(serializers.ModelSerializer):
    """Serializador simplificado para búsquedas de pacientes"""
    
    nombre_completo = serializers.SerializerMethodField()
    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = [
            'expediente', 'nombre', 'apellido_paterno', 'apellido_materno',
            'nombre_completo', 'curp', 'edad', 'genero', 'patologia', 'telefono'
        ]
    
    def get_nombre_completo(self, obj):
        return obj.get_nombre_completo()
    
    def get_edad(self, obj):
        return obj.get_edad()

class PacienteCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear pacientes con validaciones especiales"""
    
    class Meta:
        model = Paciente
        fields = [
            'expediente', 'nombre', 'apellido_paterno', 'apellido_materno',
            'curp', 'fecha_nacimiento', 'genero', 'patologia', 'cie10',
            'fecha_diagnostico', 'tipo_sangre', 'alergias', 'telefono',
            'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'numero_seguro_social',
            'institucion_seguro'
        ]
    
    def validate(self, attrs):
        """Validaciones cruzadas"""
        # Verificar que el expediente y CURP no existan
        expediente = attrs.get('expediente', '').upper()
        curp = attrs.get('curp', '').upper()
        
        if Paciente.objects.filter(expediente=expediente).exists():
            raise serializers.ValidationError({
                'expediente': f"Ya existe un paciente con el expediente {expediente}"
            })
        
        if Paciente.objects.filter(curp=curp).exists():
            existing_patient = Paciente.objects.get(curp=curp)
            raise serializers.ValidationError({
                'curp': f"Ya existe un paciente con esta CURP (Expediente: {existing_patient.expediente})"
            })
        
        return attrs
    
    def create(self, validated_data):
        """Crear paciente asignando el usuario que lo creó"""
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        
        return super().create(validated_data)

class PacienteUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar pacientes"""
    
    class Meta:
        model = Paciente
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno',
            'telefono', 'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'alergias', 'tipo_sangre',
            'numero_seguro_social', 'institucion_seguro', 'is_active'
        ]
    
    def update(self, instance, validated_data):
        """Actualizar paciente asignando el usuario que lo actualizó"""
        request = self.context.get('request')
        if request and request.user:
            validated_data['updated_by'] = request.user
        
        return super().update(instance, validated_data)


class CIE10MexicoSerializer(serializers.ModelSerializer):
    """Serializador para el catálogo CIE-10 México"""
    
    class Meta:
        model = CIE10Mexico
        fields = [
            'codigo', 'descripcion', 'descripcion_corta', 'capitulo',
            'categoria', 'tipo', 'genero_aplicable', 'edad_minima',
            'edad_maxima', 'es_mortalidad', 'es_morbilidad', 'activo'
        ]
        read_only_fields = [
            'codigo', 'descripcion', 'descripcion_corta', 'capitulo',
            'categoria', 'tipo', 'genero_aplicable', 'edad_minima',
            'edad_maxima', 'es_mortalidad', 'es_morbilidad'
        ]


class CIE10MexicoBusquedaSerializer(serializers.ModelSerializer):
    """Serializador simplificado para búsquedas de CIE-10"""
    
    descripcion_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CIE10Mexico
        fields = [
            'codigo', 'descripcion_corta', 'descripcion_display',
            'capitulo', 'tipo'
        ]
    
    def get_descripcion_display(self, obj):
        return obj.get_descripcion_display()
