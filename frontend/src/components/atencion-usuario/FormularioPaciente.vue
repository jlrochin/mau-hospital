<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-background-card rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex-shrink-0">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-secondary-900">
            {{ isEditing ? 'Editar Paciente' : 'Nuevo Paciente' }}
          </h2>
          <button
            @click="$emit('close')"
            class="text-secondary-400 hover:text-secondary-600"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Contenido scrolleable -->
      <div class="modal-scrollable p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Información Básica -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-secondary-900">
                Información Básica
              </h3>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">
                    Número de Expediente *
                  </label>
                  <input
                    v-model="form.expediente"
                    type="text"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.expediente }"
                    placeholder="Ej: EXP-2024-001"
                    :disabled="isEditing"
                    @blur="checkDuplicates"
                  />
                  <p v-if="errors.expediente" class="form-error">
                    {{ errors.expediente }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    CURP *
                  </label>
                  <input
                    v-model="form.curp"
                    type="text"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.curp }"
                    placeholder="Ej: ABCD123456HMCLEF01"
                    maxlength="18"
                    @input="formatCURP"
                    @blur="checkDuplicates"
                  />
                  <p v-if="errors.curp" class="form-error">
                    {{ errors.curp }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Nombre(s) *
                  </label>
                  <input
                    v-model="form.nombre"
                    type="text"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.nombre }"
                    placeholder="Nombre(s) del paciente"
                  />
                  <p v-if="errors.nombre" class="form-error">
                    {{ errors.nombre }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Apellido Paterno *
                  </label>
                  <input
                    v-model="form.apellido_paterno"
                    type="text"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.apellido_paterno }"
                    placeholder="Apellido paterno"
                  />
                  <p v-if="errors.apellido_paterno" class="form-error">
                    {{ errors.apellido_paterno }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Apellido Materno
                  </label>
                  <input
                    v-model="form.apellido_materno"
                    type="text"
                    class="form-input"
                    placeholder="Apellido materno"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Fecha de Nacimiento *
                  </label>
                  <input
                    v-model="form.fecha_nacimiento"
                    type="date"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.fecha_nacimiento }"
                  />
                  <p v-if="errors.fecha_nacimiento" class="form-error">
                    {{ errors.fecha_nacimiento }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Género *
                  </label>
                  <select
                    v-model="form.genero"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.genero }"
                  >
                    <option value="">Seleccionar género</option>
                    <option value="M">Masculino</option>
                    <option value="F">Femenino</option>
                    <option value="O">Otro</option>
                  </select>
                  <p v-if="errors.genero" class="form-error">
                    {{ errors.genero }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Tipo de Sangre
                  </label>
                  <select v-model="form.tipo_sangre" class="form-input">
                    <option value="ND">No Determinado</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Información Médica -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-secondary-900">
                Información Médica
              </h3>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">
                    Patología Principal *
                  </label>
                  <input
                    v-model="form.patologia"
                    type="text"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.patologia }"
                    placeholder="Ej: Diabetes Mellitus tipo 2"
                  />
                  <p v-if="errors.patologia" class="form-error">
                    {{ errors.patologia }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Código CIE-10 *
                  </label>
                  <SelectorCIE10
                    v-model="form.cie10"
                    :error-message="errors.cie10"
                    placeholder="Buscar código CIE-10..."
                    @code-selected="handleCIE10Selected"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Fecha de Diagnóstico *
                  </label>
                  <input
                    v-model="form.fecha_diagnostico"
                    type="date"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.fecha_diagnostico }"
                  />
                  <p v-if="errors.fecha_diagnostico" class="form-error">
                    {{ errors.fecha_diagnostico }}
                  </p>
                </div>

                <div class="md:col-span-2">
                  <label class="form-label">
                    Alergias Conocidas
                  </label>
                  <textarea
                    v-model="form.alergias"
                    class="form-input"
                    rows="3"
                    placeholder="Describir alergias conocidas del paciente..."
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Información de Contacto -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-secondary-900">
                Información de Contacto
              </h3>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">
                    Teléfono
                  </label>
                  <input
                    v-model="form.telefono"
                    type="tel"
                    class="form-input"
                    placeholder="Ej: 5551234567"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Contacto de Emergencia
                  </label>
                  <input
                    v-model="form.contacto_emergencia_nombre"
                    type="text"
                    class="form-input"
                    placeholder="Nombre del contacto de emergencia"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Teléfono de Emergencia
                  </label>
                  <input
                    v-model="form.contacto_emergencia_telefono"
                    type="tel"
                    class="form-input"
                    placeholder="Teléfono del contacto de emergencia"
                  />
                </div>

                <div class="md:col-span-2">
                  <label class="form-label">
                    Dirección
                  </label>
                  <textarea
                    v-model="form.direccion"
                    class="form-input"
                    rows="2"
                    placeholder="Dirección completa del paciente..."
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Información del Seguro -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-secondary-900">
                Información del Seguro Médico
              </h3>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">
                    Número de Seguro Social
                  </label>
                  <input
                    v-model="form.numero_seguro_social"
                    type="text"
                    class="form-input"
                    placeholder="Número de seguro social"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Institución de Seguro
                  </label>
                  <select v-model="form.institucion_seguro" class="form-input">
                    <option value="">Seleccionar institución</option>
                    <option value="IMSS">IMSS</option>
                    <option value="ISSSTE">ISSSTE</option>
                    <option value="PEMEX">PEMEX</option>
                    <option value="SEDENA">SEDENA</option>
                    <option value="SEMAR">SEMAR</option>
                    <option value="Seguro Popular">Seguro Popular</option>
                    <option value="INSABI">INSABI</option>
                    <option value="Particular">Particular</option>
                    <option value="Otro">Otro</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Alertas de duplicados -->
          <div v-if="duplicateWarnings.length > 0" class="bg-warning bg-opacity-10 border border-warning rounded-lg p-4">
            <div class="flex">
              <ExclamationTriangleIcon class="h-5 w-5 text-warning" />
              <div class="ml-3">
                <h3 class="text-sm font-medium text-warning">
                  Advertencia: Posibles duplicados
                </h3>
                <div class="mt-2 text-sm text-warning">
                  <ul class="list-disc list-inside">
                    <li v-for="warning in duplicateWarnings" :key="warning.campo">
                      Ya existe un paciente con {{ warning.campo.toUpperCase() }}: {{ warning.valor }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

        </form>
      </div>

      <!-- Footer con botones -->
      <div class="px-6 py-4 border-t border-gray-200 flex-shrink-0">
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="$emit('close')"
            class="btn-secondary"
          >
            Cancelar
          </button>
          <button
            type="button"
            @click="handleSubmit"
            :disabled="isSubmitting || duplicateWarnings.length > 0"
            class="btn-primary"
          >
            <span v-if="isSubmitting">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Guardando...
            </span>
            <span v-else>
              {{ isEditing ? 'Actualizar' : 'Crear' }} Paciente
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'
import {
  XMarkIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import SelectorCIE10 from '@/components/shared/SelectorCIE10.vue'

export default {
  name: 'FormularioPaciente',
  components: {
    XMarkIcon,
    ExclamationTriangleIcon,
    SelectorCIE10
  },
  props: {
    patient: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const toast = useToast()
    
    const isSubmitting = ref(false)
    const duplicateWarnings = ref([])
    
    const isEditing = computed(() => !!props.patient)
    
    const form = reactive({
      expediente: '',
      curp: '',
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      fecha_nacimiento: '',
      genero: '',
      patologia: '',
      cie10: '',
      fecha_diagnostico: '',
      tipo_sangre: 'ND',
      alergias: '',
      telefono: '',
      direccion: '',
      contacto_emergencia_nombre: '',
      contacto_emergencia_telefono: '',
      numero_seguro_social: '',
      institucion_seguro: ''
    })
    
    const errors = reactive({})
    
    // Cargar datos del paciente si está editando
    onMounted(() => {
      if (props.patient) {
        Object.keys(form).forEach(key => {
          if (props.patient[key] !== undefined) {
            form[key] = props.patient[key]
          }
        })
      }
    })
    
    const formatCURP = () => {
      form.curp = form.curp.toUpperCase()
    }
    
    const validateForm = () => {
      const newErrors = {}
      
      // Campos requeridos
      const requiredFields = [
        'expediente', 'curp', 'nombre', 'apellido_paterno',
        'fecha_nacimiento', 'genero', 'patologia', 'cie10', 'fecha_diagnostico'
      ]
      
      requiredFields.forEach(field => {
        if (!form[field]?.trim()) {
          newErrors[field] = 'Este campo es requerido'
        }
      })
      
      // Validación específica de CURP
      if (form.curp && !/^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$/.test(form.curp)) {
        newErrors.curp = 'CURP inválida'
      }
      
      // Validación de fecha de nacimiento
      if (form.fecha_nacimiento) {
        const birthDate = new Date(form.fecha_nacimiento)
        const today = new Date()
        if (birthDate > today) {
          newErrors.fecha_nacimiento = 'La fecha de nacimiento no puede ser futura'
        }
      }
      
      // Validación de fecha de diagnóstico
      if (form.fecha_diagnostico) {
        const diagDate = new Date(form.fecha_diagnostico)
        const today = new Date()
        if (diagDate > today) {
          newErrors.fecha_diagnostico = 'La fecha de diagnóstico no puede ser futura'
        }
      }
      
      Object.assign(errors, newErrors)
      return Object.keys(newErrors).length === 0
    }
    
    const checkDuplicates = async () => {
      if (!form.expediente.trim() && !form.curp.trim()) return
      
      try {
        const response = await api.get('/pacientes/verificar-duplicados/', {
          params: {
            expediente: form.expediente.trim(),
            curp: form.curp.trim()
          }
        })
        
        duplicateWarnings.value = response.data.duplicados || []
      } catch (error) {
        console.error('Error checking duplicates:', error)
      }
    }
    
    const handleCIE10Selected = (code) => {
      if (code) {
        // Auto-completar la patología si está vacía
        if (!form.patologia.trim()) {
          form.patologia = code.descripcion_corta
        }
      }
    }

    const handleSubmit = async () => {
      if (!validateForm()) {
        toast.error('Por favor corrige los errores en el formulario')
        return
      }
      
      if (duplicateWarnings.value.length > 0 && !isEditing.value) {
        toast.error('Hay duplicados que deben resolverse antes de continuar')
        return
      }
      
      try {
        isSubmitting.value = true
        
        const endpoint = isEditing.value 
          ? `/pacientes/${props.patient.expediente}/`
          : '/pacientes/'
        
        const method = isEditing.value ? 'patch' : 'post'
        
        const response = await api[method](endpoint, form)
        
        emit('saved', response.data)
        toast.success(`Paciente ${isEditing.value ? 'actualizado' : 'creado'} correctamente`)
        
      } catch (error) {
        console.error('Error saving patient:', error)
        
        if (error.response?.data) {
          const errorData = error.response.data
          
          // Manejar errores de campo específicos
          Object.keys(errorData).forEach(field => {
            if (errors.hasOwnProperty(field)) {
              errors[field] = Array.isArray(errorData[field]) 
                ? errorData[field][0] 
                : errorData[field]
            }
          })
        }
        
        toast.error('Error al guardar el paciente')
      } finally {
        isSubmitting.value = false
      }
    }
    
    return {
      form,
      errors,
      isSubmitting,
      duplicateWarnings,
      isEditing,
      formatCURP,
      checkDuplicates,
      handleCIE10Selected,
      handleSubmit
    }
  }
}
</script>
