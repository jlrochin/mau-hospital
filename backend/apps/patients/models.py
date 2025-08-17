from django.db import models
from django.core.validators import RegexValidator

class CIE10Mexico(models.Model):
    """Catálogo oficial CIE-10 autorizado en México"""
    
    codigo = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name='Código CIE-10',
        help_text='Código oficial CIE-10 (ej: A00.0, B15.9, etc.)'
    )
    
    descripcion = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción completa del diagnóstico'
    )
    
    descripcion_corta = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Descripción Corta',
        help_text='Versión abreviada de la descripción'
    )
    
    capitulo = models.CharField(
        max_length=5,
        verbose_name='Capítulo',
        help_text='Capítulo del CIE-10 (I-XXII)'
    )
    
    categoria = models.CharField(
        max_length=10,
        verbose_name='Categoría',
        help_text='Categoría del código (primeros 3 caracteres)'
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('ENFERMEDAD', 'Enfermedad'),
            ('TRAUMATISMO', 'Traumatismo y envenenamiento'),
            ('FACTOR_EXTERNO', 'Causas externas'),
            ('FACTOR_SALUD', 'Factores que influyen en el estado de salud'),
        ],
        verbose_name='Tipo de código'
    )
    
    genero_aplicable = models.CharField(
        max_length=10,
        choices=[
            ('AMBOS', 'Ambos géneros'),
            ('MASCULINO', 'Solo masculino'),
            ('FEMENINO', 'Solo femenino'),
        ],
        default='AMBOS',
        verbose_name='Género aplicable'
    )
    
    edad_minima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Edad mínima',
        help_text='Edad mínima en años para aplicar este diagnóstico'
    )
    
    edad_maxima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Edad máxima',
        help_text='Edad máxima en años para aplicar este diagnóstico'
    )
    
    es_mortalidad = models.BooleanField(
        default=False,
        verbose_name='Es causa de mortalidad',
        help_text='Indica si este código puede ser causa básica de muerte'
    )
    
    es_morbilidad = models.BooleanField(
        default=True,
        verbose_name='Es causa de morbilidad',
        help_text='Indica si este código puede usarse para morbilidad'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'CIE-10 México'
        verbose_name_plural = 'CIE-10 México'
        db_table = 'cie10_mexico'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria']),
            models.Index(fields=['capitulo']),
            models.Index(fields=['tipo']),
            models.Index(fields=['descripcion']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion_corta or self.descripcion[:50]}"
    
    def get_descripcion_display(self):
        """Retorna la descripción más apropiada"""
        return self.descripcion_corta or self.descripcion
    
    def is_aplicable_for_patient(self, paciente):
        """Verifica si este código CIE-10 es aplicable para un paciente específico"""
        # Verificar género
        if self.genero_aplicable != 'AMBOS':
            if self.genero_aplicable == 'MASCULINO' and paciente.genero != 'M':
                return False
            if self.genero_aplicable == 'FEMENINO' and paciente.genero != 'F':
                return False
        
        # Verificar edad
        edad_paciente = paciente.get_edad()
        if self.edad_minima and edad_paciente < self.edad_minima:
            return False
        if self.edad_maxima and edad_paciente > self.edad_maxima:
            return False
        
        return True


class Paciente(models.Model):
    """Modelo para gestionar pacientes del hospital"""
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('ND', 'No Determinado'),
    ]
    
    # Campo EXPEDIENTE como Primary Key
    expediente = models.CharField(
        max_length=20,
        primary_key=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9-]+$',
            message='El expediente debe contener solo letras mayúsculas, números y guiones'
        )],
        verbose_name='Número de Expediente',
        help_text='Identificador único del paciente'
    )
    
    # Información personal
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre(s)'
    )
    
    apellido_paterno = models.CharField(
        max_length=100,
        verbose_name='Apellido Paterno'
    )
    
    apellido_materno = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Apellido Materno'
    )
    
    curp = models.CharField(
        max_length=18,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$',
            message='CURP inválida. Formato: 4 letras, 6 números, H/M, 5 letras, 2 números'
        )],
        verbose_name='CURP'
    )
    
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento'
    )
    
    genero = models.CharField(
        max_length=1,
        choices=GENERO_CHOICES,
        verbose_name='Género'
    )
    
    # Información médica
    patologia = models.CharField(
        max_length=200,
        verbose_name='Patología Principal'
    )
    
    cie10 = models.CharField(
        max_length=10,
        verbose_name='Código CIE-10',
        help_text='Clasificación Internacional de Enfermedades'
    )
    
    # Relación opcional con el catálogo oficial CIE-10
    cie10_oficial = models.ForeignKey(
        'CIE10Mexico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='CIE-10 Oficial',
        help_text='Relación con el catálogo oficial CIE-10 México'
    )
    
    fecha_diagnostico = models.DateField(
        verbose_name='Fecha de Diagnóstico'
    )
    
    tipo_sangre = models.CharField(
        max_length=3,
        choices=TIPO_SANGRE_CHOICES,
        default='ND',
        verbose_name='Tipo de Sangre'
    )
    
    alergias = models.TextField(
        blank=True,
        null=True,
        verbose_name='Alergias Conocidas'
    )
    
    # Información de contacto
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Número de teléfono inválido'
        )],
        verbose_name='Teléfono'
    )
    
    direccion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    
    contacto_emergencia_nombre = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nombre del Contacto de Emergencia'
    )
    
    contacto_emergencia_telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Número de teléfono inválido'
        )],
        verbose_name='Teléfono del Contacto de Emergencia'
    )
    
    # Información del seguro médico
    numero_seguro_social = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Número de Seguro Social'
    )
    
    institucion_seguro = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Institución de Seguro',
        help_text='IMSS, ISSSTE, Seguro Popular, etc.'
    )
    
    # Metadatos
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    # Usuario que creó y actualizó el registro
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pacientes_creados',
        verbose_name='Creado por'
    )
    
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='pacientes_actualizados',
        verbose_name='Actualizado por'
    )
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        db_table = 'pacientes'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']
        indexes = [
            models.Index(fields=['curp']),
            models.Index(fields=['nombre', 'apellido_paterno']),
            models.Index(fields=['fecha_nacimiento']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.expediente} - {self.get_nombre_completo()}"
    
    def get_nombre_completo(self):
        """Retorna el nombre completo del paciente"""
        nombres = [self.nombre, self.apellido_paterno]
        if self.apellido_materno:
            nombres.append(self.apellido_materno)
        return ' '.join(nombres)
    
    def get_edad(self):
        """Calcula la edad del paciente"""
        from datetime import date
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < 
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    def save(self, *args, **kwargs):
        """Override del método save para normalizar datos"""
        # Convertir CURP a mayúsculas
        if self.curp:
            self.curp = self.curp.upper()
        
        # Convertir expediente a mayúsculas
        if self.expediente:
            self.expediente = self.expediente.upper()
        
        # Capitalizar nombres
        if self.nombre:
            self.nombre = self.nombre.title()
        if self.apellido_paterno:
            self.apellido_paterno = self.apellido_paterno.title()
        if self.apellido_materno:
            self.apellido_materno = self.apellido_materno.title()
        
        super().save(*args, **kwargs)
