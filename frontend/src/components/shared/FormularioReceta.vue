<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-background-card rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex-shrink-0">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-secondary-900">
            Nueva Receta para {{ patient.nombre }} {{ patient.apellido_paterno }} {{ patient.apellido_materno || '' }}
          </h2>
          <button
            @click="$emit('close')"
            class="text-secondary-400 hover:text-secondary-600"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="mt-2 text-sm text-secondary-600">
          <span class="font-medium">Expediente:</span> {{ patient.expediente }} |
          <span class="font-medium">CURP:</span> {{ patient.curp }}
        </div>
      </div>

      <!-- Contenido scrolleable -->
      <div class="modal-scrollable p-6">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Información básica de la receta -->
          <div class="card">
            <div class="card-header">
              <h3 class="text-lg font-medium text-secondary-900">
                Información de la Receta
              </h3>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">
                    Tipo de Receta *
                  </label>
                  <select
                    v-model="form.tipo_receta"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.tipo_receta }"
                  >
                    <option value="">Seleccionar tipo</option>
                    <option value="FARMACIA">Farmacia</option>
                    <option value="CMI">Centro de Mezclas (CMI)</option>
                  </select>
                  <p v-if="errors.tipo_receta" class="form-error">
                    {{ errors.tipo_receta }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Prioridad *
                  </label>
                  <select
                    v-model="form.prioridad"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.prioridad }"
                  >
                    <option value="">Seleccionar prioridad</option>
                    <option value="BAJA">Baja</option>
                    <option value="MEDIA">Media</option>
                    <option value="ALTA">Alta</option>
                    <option value="URGENTE">Urgente</option>
                  </select>
                  <p v-if="errors.prioridad" class="form-error">
                    {{ errors.prioridad }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Servicio Solicitante *
                  </label>
                  <select
                    v-model="form.servicio_solicitante"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.servicio_solicitante }"
                  >
                    <option value="">Seleccionar servicio</option>
                    <option value="Oncología">Oncología</option>
                    <option value="Medicina Interna">Medicina Interna</option>
                    <option value="Urgencias">Urgencias</option>
                    <option value="Cardiología">Cardiología</option>
                    <option value="Neurología">Neurología</option>
                    <option value="Pediatría">Pediatría</option>
                    <option value="Ginecología">Ginecología</option>
                    <option value="Cirugía">Cirugía</option>
                  </select>
                  <p v-if="errors.servicio_solicitante" class="form-error">
                    {{ errors.servicio_solicitante }}
                  </p>
                </div>

                <div>
                  <label class="form-label">
                    Fecha de Vencimiento
                  </label>
                  <input
                    v-model="form.fecha_vencimiento"
                    type="date"
                    class="form-input"
                    :min="minDate"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Código CIE-10
                  </label>
                  <SelectorCIE10
                    v-model="form.cie10"
                    placeholder="Buscar código CIE-10..."
                    @code-selected="handleCIE10Selected"
                  />
                </div>

                <div>
                  <label class="form-label">
                    Diagnóstico *
                  </label>
                  <textarea
                    v-model="form.diagnostico"
                    class="form-input"
                    :class="{ 'border-accent-500': errors.diagnostico }"
                    rows="2"
                    placeholder="Diagnóstico asociado a la receta..."
                  ></textarea>
                  <p v-if="errors.diagnostico" class="form-error">
                    {{ errors.diagnostico }}
                  </p>
                </div>

                <div class="md:col-span-2">
                  <label class="form-label">
                    Indicaciones Generales
                  </label>
                  <textarea
                    v-model="form.indicaciones_generales"
                    class="form-input"
                    rows="2"
                    placeholder="Instrucciones especiales para el paciente..."
                  ></textarea>
                </div>
              </div>
            </div>
          </div>

          <!-- Medicamentos -->
          <div class="card">
            <div class="card-header">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-gray-900">
                  Medicamentos
                </h3>
                <button
                  type="button"
                  @click="addMedicamento"
                  class="btn-primary text-sm"
                  :disabled="!form.tipo_receta"
                >
                  <PlusIcon class="h-4 w-4 mr-1" />
                  Agregar Medicamento
                </button>
              </div>
            </div>
            <div class="card-body">
              <div v-if="form.detalles.length === 0" class="text-center py-8 text-gray-500">
                <div v-if="!form.tipo_receta" class="mb-4">
                  <ExclamationTriangleIcon class="h-12 w-12 mx-auto text-warning" />
                  <p class="mt-2">Primero selecciona el tipo de receta para agregar medicamentos</p>
                </div>
                <div v-else>
                  <PlusIcon class="h-12 w-12 mx-auto text-gray-400" />
                  <p class="mt-2">No hay medicamentos agregados. Haz clic en "Agregar Medicamento" para comenzar.</p>
                </div>
              </div>
              
              <div v-else class="space-y-6">
                <div
                  v-for="(medicamento, index) in form.detalles"
                  :key="index"
                  class="border border-gray-200 rounded-lg p-6 bg-gray-50"
                >
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="font-medium text-gray-900">
                      Medicamento {{ index + 1 }}
                    </h4>
                    <button
                      type="button"
                      @click="removeMedicamento(index)"
                      class="text-accent-500 hover:text-accent-600 p-2 rounded-lg hover:bg-red-50 transition-colors"
                      title="Eliminar medicamento"
                    >
                      <TrashIcon class="h-5 w-5" />
                    </button>
                  </div>
                  
                  <!-- Selector de medicamento mejorado -->
                  <SelectorMedicamento
                    :tipo-receta="form.tipo_receta"
                    :model-value="medicamento.selector_data"
                    @update:model-value="updateMedicamento(index, $event)"
                    @medicamento-selected="onMedicamentoSelected(index, $event)"
                  />

                  <!-- Campos adicionales opcionales -->
                  <div v-if="medicamento.selector_data" class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        Frecuencia (opcional)
                      </label>
                      <input
                        v-model="medicamento.frecuencia"
                        type="text"
                        class="form-input"
                        placeholder="Ej: Cada 8 horas"
                      />
                    </div>

                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        Duración del Tratamiento (opcional)
                      </label>
                      <input
                        v-model="medicamento.duracion_tratamiento"
                        type="text"
                        class="form-input"
                        placeholder="Ej: 7 días, 2 semanas"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Observaciones -->
          <div class="card">
            <div class="card-body">
              <label class="form-label">
                Observaciones Generales
              </label>
              <textarea
                v-model="form.observaciones"
                class="form-input"
                rows="3"
                placeholder="Observaciones adicionales sobre la receta..."
              ></textarea>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200">
            <button
              type="button"
              @click="$emit('close')"
              class="btn-secondary"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="isSubmitting || form.detalles.length === 0"
              class="btn-primary"
            >
              <span v-if="isSubmitting">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creando receta...
              </span>
              <span v-else>
                Crear Receta
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { format, addDays } from 'date-fns'
import api from '@/services/api'
import {
  XMarkIcon,
  PlusIcon,
  TrashIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import SelectorMedicamento from './SelectorMedicamento.vue'
import SelectorCIE10 from './SelectorCIE10.vue'

export default {
  name: 'FormularioReceta',
  components: {
    XMarkIcon,
    PlusIcon,
    TrashIcon,
    ExclamationTriangleIcon,
    SelectorMedicamento,
    SelectorCIE10
  },
  props: {
    patient: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'saved'],
  setup(props, { emit }) {
    const toast = useToast()
    
    const isSubmitting = ref(false)
    
    const form = reactive({
      paciente: props.patient.expediente,
      tipo_receta: 'FARMACIA',
      prioridad: 'MEDIA',
      servicio_solicitante: '',
      cie10: '',
      diagnostico: '',
      indicaciones_generales: '',
      fecha_vencimiento: '',
      observaciones: '',
      detalles: []
    })
    
    const errors = reactive({})
    
    const minDate = computed(() => {
      return format(new Date(), 'yyyy-MM-dd')
    })
    
    const addMedicamento = () => {
      form.detalles.push({
        selector_data: null,
        clave_medicamento: '',
        descripcion_medicamento: '',
        dosis: '',
        cantidad_prescrita: 1,
        frecuencia: '',
        duracion_tratamiento: ''
      })
    }
    
    const updateMedicamento = (index, selectorData) => {
      const medicamento = form.detalles[index]
      medicamento.selector_data = selectorData
      
      if (selectorData) {
        // Auto-rellenar campos desde el selector
        medicamento.clave_medicamento = selectorData.medicamento.clave
        medicamento.descripcion_medicamento = selectorData.medicamento.nombre
        medicamento.dosis = selectorData.dosis
        medicamento.cantidad_prescrita = selectorData.cantidad_prescrita
      } else {
        // Limpiar campos si se deselecciona
        medicamento.clave_medicamento = ''
        medicamento.descripcion_medicamento = ''
        medicamento.dosis = ''
        medicamento.cantidad_prescrita = 1
      }
    }
    
    const onMedicamentoSelected = (index, medicamento) => {
      console.log('Medicamento seleccionado:', medicamento)
      // El updateMedicamento ya maneja la actualización
    }

    const handleCIE10Selected = (code) => {
      if (code) {
        // Auto-completar el diagnóstico si está vacío
        if (!form.diagnostico.trim()) {
          form.diagnostico = code.descripcion_corta
        }
      }
    }
    
    const removeMedicamento = (index) => {
      form.detalles.splice(index, 1)
    }
    
    const validateForm = () => {
      const newErrors = {}
      
      // Campos requeridos de la receta
      const requiredFields = [
        'tipo_receta', 'prioridad', 'servicio_solicitante', 'diagnostico'
      ]
      
      requiredFields.forEach(field => {
        if (!form[field]?.trim()) {
          newErrors[field] = 'Este campo es requerido'
        }
      })
      
      // Validar que haya al menos un medicamento
      if (form.detalles.length === 0) {
        newErrors.detalles = 'Debe agregar al menos un medicamento'
      }
      
      // Validar cada medicamento
      form.detalles.forEach((medicamento, index) => {
        if (!medicamento.selector_data) {
          newErrors[`medicamento_${index}_selector`] = 'Debe seleccionar un medicamento del catálogo'
        } else {
          if (!medicamento.dosis?.trim()) {
            newErrors[`medicamento_${index}_dosis`] = 'Dosis requerida'
          }
          if (!medicamento.cantidad_prescrita || medicamento.cantidad_prescrita < 1) {
            newErrors[`medicamento_${index}_cantidad`] = 'Cantidad inválida'
          }
        }
      })
      
      // Validar fecha de vencimiento
      if (form.fecha_vencimiento) {
        const fechaVencimiento = new Date(form.fecha_vencimiento)
        const hoy = new Date()
        hoy.setHours(0, 0, 0, 0)
        
        if (fechaVencimiento <= hoy) {
          newErrors.fecha_vencimiento = 'La fecha de vencimiento debe ser futura'
        }
      }
      
      Object.assign(errors, newErrors)
      return Object.keys(newErrors).length === 0
    }
    
    const handleSubmit = async () => {
      if (!validateForm()) {
        toast.error('Por favor corrige los errores en el formulario')
        return
      }
      
      try {
        isSubmitting.value = true
        
        const response = await api.post('/recetas/', form)
        
        emit('saved', response.data)
        toast.success('Receta creada correctamente')
        
      } catch (error) {
        console.error('Error creating recipe:', error)
        
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
        
        toast.error('Error al crear la receta')
      } finally {
        isSubmitting.value = false
      }
    }
    
    // Agregar un medicamento por defecto
    addMedicamento()
    
    return {
      form,
      errors,
      isSubmitting,
      minDate,
      addMedicamento,
      removeMedicamento,
      updateMedicamento,
      onMedicamentoSelected,
      handleCIE10Selected,
      handleSubmit
    }
  }
}
</script>
