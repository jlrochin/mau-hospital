from rest_framework import serializers
from .models import Paciente, CIE10Mexico, PacienteCIE10

class PacienteCIE10Serializer(serializers.ModelSerializer):
    """Serializador para los códigos CIE-10 de un paciente"""
    
    cie10_info = serializers.SerializerMethodField()
    
    class Meta:
        model = PacienteCIE10
        fields = [
            'id', 'cie10', 'cie10_info', 'fecha_diagnostico', 
            'es_principal', 'observaciones', 'created_at'
        ]
    
    def get_cie10_info(self, obj):
        """Obtener información del código CIE-10"""
        return {
            'codigo': obj.cie10.codigo,
            'descripcion_corta': obj.cie10.descripcion_corta,
            'descripcion': obj.cie10.descripcion,
            'capitulo': obj.cie10.capitulo,
            'tipo': obj.cie10.tipo
        }

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
    
    cie10_codes = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text='Lista de códigos CIE-10 para el paciente'
    )
    
    class Meta:
        model = Paciente
        fields = [
            'expediente', 'nombre', 'apellido_paterno', 'apellido_materno',
            'curp', 'fecha_nacimiento', 'genero', 'patologia', 'cie10',
            'fecha_diagnostico', 'tipo_sangre', 'alergias', 'telefono',
            'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'numero_seguro_social',
            'institucion_seguro', 'cie10_codes'
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
        
        # Validar códigos CIE-10 si se proporcionan
        cie10_codes = attrs.get('cie10_codes', [])
        if cie10_codes:
            # Verificar que al menos uno sea marcado como principal
            tiene_principal = any(code.get('es_principal', False) for code in cie10_codes)
            if not tiene_principal:
                raise serializers.ValidationError({
                    'cie10_codes': 'Al menos un código CIE-10 debe ser marcado como diagnóstico principal'
                })
            
            # Verificar que solo haya un diagnóstico principal
            principales = [code for code in cie10_codes if code.get('es_principal', False)]
            if len(principales) > 1:
                raise serializers.ValidationError({
                    'cie10_codes': 'Solo puede haber un diagnóstico principal'
                })
        
        return attrs
    
    def create(self, validated_data):
        """Crear paciente asignando el usuario que lo creó"""
        cie10_codes = validated_data.pop('cie10_codes', [])
        
        request = self.context.get('request')
        if request and request.user:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        
        # Crear el paciente
        paciente = super().create(validated_data)
        
        # Crear los códigos CIE-10 si se proporcionaron
        if cie10_codes:
            for cie10_data in cie10_codes:
                # Obtener el código CIE-10
                try:
                    cie10 = CIE10Mexico.objects.get(codigo=cie10_data['cie10'])
                except CIE10Mexico.DoesNotExist:
                    continue
                
                # Crear el PacienteCIE10
                PacienteCIE10.objects.create(
                    paciente=paciente,
                    cie10=cie10,
                    fecha_diagnostico=cie10_data.get('fecha_diagnostico', validated_data.get('fecha_diagnostico')),
                    es_principal=cie10_data.get('es_principal', False),
                    observaciones=cie10_data.get('observaciones', '')
                )
        
        return paciente

class PacienteCIE10CreateSerializer(serializers.ModelSerializer):
    """Serializador para crear códigos CIE-10 para un paciente"""
    
    class Meta:
        model = PacienteCIE10
        fields = [
            'cie10', 'fecha_diagnostico', 'es_principal', 'observaciones'
        ]
    
    def validate(self, attrs):
        """Validar que solo haya un diagnóstico principal por paciente"""
        paciente = self.context.get('paciente')
        es_principal = attrs.get('es_principal', False)
        
        if es_principal:
            # Verificar que no haya otro diagnóstico principal
            if PacienteCIE10.objects.filter(
                paciente=paciente, 
                es_principal=True
            ).exclude(id=self.instance.id if self.instance else None).exists():
                raise serializers.ValidationError(
                    "Ya existe un diagnóstico principal para este paciente"
                )
        
        return attrs


class PacienteUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar pacientes"""
    
    cie10_codes = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text='Lista de códigos CIE-10 para el paciente'
    )
    
    class Meta:
        model = Paciente
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'genero', 'patologia', 'cie10', 'fecha_diagnostico',
            'telefono', 'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'alergias', 'tipo_sangre',
            'numero_seguro_social', 'institucion_seguro', 'is_active', 'cie10_codes'
        ]
    
    def validate(self, attrs):
        """Validaciones para códigos CIE-10"""
        cie10_codes = attrs.get('cie10_codes', [])
        if cie10_codes:
            # Verificar que al menos uno sea marcado como principal
            tiene_principal = any(code.get('es_principal', False) for code in cie10_codes)
            if not tiene_principal:
                raise serializers.ValidationError({
                    'cie10_codes': 'Al menos un código CIE-10 debe ser marcado como diagnóstico principal'
                })
            
            # Verificar que solo haya un diagnóstico principal
            principales = [code for code in cie10_codes if code.get('es_principal', False)]
            if len(principales) > 1:
                raise serializers.ValidationError({
                    'cie10_codes': 'Solo puede haber un diagnóstico principal'
                })
        
        return attrs
    
    def update(self, instance, validated_data):
        """Actualizar paciente asignando el usuario que lo actualizó"""
        cie10_codes = validated_data.pop('cie10_codes', None)
        
        request = self.context.get('request')
        if request and request.user:
            validated_data['updated_by'] = request.user
        
        # Actualizar el paciente
        paciente = super().update(instance, validated_data)
        
        # Actualizar códigos CIE-10 si se proporcionaron
        if cie10_codes is not None:
            # Eliminar códigos existentes
            PacienteCIE10.objects.filter(paciente=paciente).delete()
            
            # Crear los nuevos códigos
            if cie10_codes:
                for cie10_data in cie10_codes:
                    try:
                        cie10 = CIE10Mexico.objects.get(codigo=cie10_data['cie10'])
                    except CIE10Mexico.DoesNotExist:
                        continue
                    
                    # Crear el PacienteCIE10
                    PacienteCIE10.objects.create(
                        paciente=paciente,
                        cie10=cie10,
                        fecha_diagnostico=cie10_data.get('fecha_diagnostico', validated_data.get('fecha_diagnostico')),
                        es_principal=cie10_data.get('es_principal', False),
                        observaciones=cie10_data.get('observaciones', '')
                    )
        
        return paciente


class CIE10MexicoSerializer(serializers.ModelSerializer):
    """Serializador para el catálogo CIE-10 México con todos los campos"""
    
    class Meta:
        model = CIE10Mexico
        fields = '__all__'  # Incluir todos los campos del modelo
        read_only_fields = [
            'codigo', 'descripcion', 'descripcion_corta', 'capitulo',
            'categoria', 'tipo', 'genero_aplicable', 'es_mortalidad', 
            'es_morbilidad', 'fecha_creacion', 'fecha_actualizacion'
        ]


class PacienteDetailSerializer(serializers.ModelSerializer):
    """Serializador para mostrar pacientes con múltiples códigos CIE-10"""
    
    nombre_completo = serializers.SerializerMethodField()
    edad = serializers.SerializerMethodField()
    cie10_codes = serializers.SerializerMethodField()
    diagnostico_principal = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = [
            'expediente', 'nombre', 'apellido_paterno', 'apellido_materno',
            'nombre_completo', 'curp', 'fecha_nacimiento', 'edad', 'genero',
            'patologia', 'cie10', 'fecha_diagnostico', 'tipo_sangre', 'alergias',
            'telefono', 'direccion', 'contacto_emergencia_nombre',
            'contacto_emergencia_telefono', 'numero_seguro_social',
            'institucion_seguro', 'is_active', 'created_at', 'updated_at',
            'created_by', 'updated_by', 'cie10_codes', 'diagnostico_principal'
        ]
        read_only_fields = [
            'nombre_completo', 'edad', 'created_at', 'updated_at',
            'created_by', 'updated_by', 'cie10_codes', 'diagnostico_principal'
        ]
    
    def get_nombre_completo(self, obj):
        return obj.get_nombre_completo()
    
    def get_edad(self, obj):
        return obj.get_edad()
    
    def get_cie10_codes(self, obj):
        """Obtener todos los códigos CIE-10 del paciente con información detallada"""
        cie10_codes = PacienteCIE10.objects.filter(paciente=obj).order_by('-es_principal', '-fecha_diagnostico')
        
        return [{
            'id': code.id,
            'codigo': code.cie10.codigo,
            'descripcion_corta': code.cie10.descripcion_corta,
            'descripcion': code.cie10.descripcion,
            'capitulo': code.cie10.capitulo,
            'tipo': code.cie10.tipo,
            'fecha_diagnostico': code.fecha_diagnostico,
            'es_principal': code.es_principal,
            'observaciones': code.observaciones,
            'created_at': code.created_at,
            'updated_at': code.updated_at
        } for code in cie10_codes]
    
    def get_diagnostico_principal(self, obj):
        """Obtener información del diagnóstico principal"""
        principal = PacienteCIE10.objects.filter(paciente=obj, es_principal=True).first()
        if principal:
            return {
                'codigo': principal.cie10.codigo,
                'descripcion_corta': principal.cie10.descripcion_corta,
                'descripcion': principal.cie10.descripcion,
                'fecha_diagnostico': principal.fecha_diagnostico,
                'observaciones': principal.observaciones
            }
        return None


class CIE10MexicoBusquedaSerializer(serializers.ModelSerializer):
    """Serializador para búsquedas de CIE-10 con información completa"""
    
    descripcion_mostrar = serializers.SerializerMethodField()
    tipo_mostrar = serializers.SerializerMethodField()
    genero_mostrar = serializers.SerializerMethodField()
    capitulo_mostrar = serializers.SerializerMethodField()
    aplicabilidad_mostrar = serializers.SerializerMethodField()
    
    class Meta:
        model = CIE10Mexico
        fields = [
            'codigo', 'descripcion_corta', 'descripcion_mostrar', 
            'capitulo', 'capitulo_mostrar', 'tipo', 'tipo_mostrar',
            'genero_aplicable', 'genero_mostrar', 'aplicabilidad_mostrar',
            'es_mortalidad', 'es_morbilidad', 'activo'
        ]
    
    def get_descripcion_mostrar(self, obj):
        """Retorna la descripción más apropiada para mostrar"""
        return obj.descripcion_corta or obj.descripcion[:100] + "..." if len(obj.descripcion) > 100 else obj.descripcion
    
    def get_tipo_mostrar(self, obj):
        """Retorna el tipo de código de forma legible"""
        if obj.tipo == 'ENFERMEDAD':
            return 'Enfermedad'
        elif obj.tipo == 'TRAUMATISMO':
            return 'Traumatismo'
        elif obj.tipo == 'FACTOR_EXTERNO':
            return 'Causa externa'
        elif obj.tipo == 'FACTOR_SALUD':
            return 'Factor de salud'
        else:
            return obj.tipo or 'N/A'
    
    def get_genero_mostrar(self, obj):
        """Retorna el género aplicable de forma legible"""
        if obj.genero_aplicable == 'MASCULINO':
            return 'Solo masculino'
        elif obj.genero_aplicable == 'FEMENINO':
            return 'Solo femenino'
        elif obj.genero_aplicable == 'AMBOS':
            return 'Ambos géneros'
        else:
            return obj.genero_aplicable or 'N/A'
    
    def get_capitulo_mostrar(self, obj):
        """Retorna el capítulo de forma legible"""
        if obj.capitulo:
            return f"Capítulo {obj.capitulo}"
        elif obj.clave_capitulo:
            return f"Capítulo {obj.clave_capitulo}"
        else:
            return 'N/A'
    
    def get_aplicabilidad_mostrar(self, obj):
        """Retorna la aplicabilidad del código"""
        aplicaciones = []
        if obj.es_mortalidad:
            aplicaciones.append('Mortalidad')
        if obj.es_morbilidad:
            aplicaciones.append('Morbilidad')
        
        if aplicaciones:
            return ', '.join(aplicaciones)
        else:
            return 'N/A'
