<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div class="bg-background-card rounded-xl shadow-xl max-w-6xl w-full max-h-[90vh] flex flex-col">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200 flex-shrink-0">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold text-secondary-900">
            Dispensar Receta #{{ recipe.folio_receta }} - {{ type }}
          </h2>
          <button
            @click="$emit('close')"
            class="text-secondary-400 hover:text-secondary-600"
          >
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="mt-2 text-sm text-secondary-600">
          <span class="font-medium">Paciente:</span> 
          {{ recipe.paciente_info?.nombre }} {{ recipe.paciente_info?.apellido_paterno }} {{ recipe.paciente_info?.apellido_materno || '' }} |
          <span class="font-medium">Expediente:</span> {{ recipe.paciente_info?.expediente }}
        </div>
      </div>

      <!-- Contenido scrolleable -->
      <div class="modal-scrollable p-6">
        <!-- Información de la receta -->
        <div class="card mb-6">
          <div class="card-body">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <p><span class="font-medium">Servicio:</span> {{ recipe.servicio_solicitante }}</p>
                <p><span class="font-medium">Prioridad:</span> 
                  <span class="badge" :class="getPriorityClass(recipe.prioridad)">
                    {{ recipe.prioridad }}
                  </span>
                </p>
              </div>
              <div>
                <p><span class="font-medium">Prescrito por:</span> {{ recipe.prescrito_por_name }}</p>
                <p><span class="font-medium">Validada:</span> {{ formatDate(recipe.fecha_validacion) }}</p>
              </div>
              <div>
                <p v-if="recipe.fecha_vencimiento"><span class="font-medium">Vence:</span> {{ formatDate(recipe.fecha_vencimiento) }}</p>
                <p><span class="font-medium">Total medicamentos:</span> {{ medicamentos.length }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Lista de medicamentos para dispensar -->
        <div class="space-y-4">
          <h3 class="text-lg font-medium text-secondary-900">
            Medicamentos a Dispensar
          </h3>

          <div v-if="isLoading" class="text-center py-8">
            <div class="inline-flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Cargando medicamentos...
            </div>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="medicamento in medicamentos"
              :key="medicamento.id"
              class="card"
            >
              <div class="card-body">
                <div class="flex justify-between items-start mb-4">
                  <div class="flex-1">
                    <h4 class="font-medium text-secondary-900">
                      {{ medicamento.descripcion_medicamento }}
                    </h4>
                    <p class="text-sm text-secondary-600">
                      <span class="font-medium">Clave:</span> {{ medicamento.clave_medicamento }}
                    </p>
                    <p v-if="medicamento.concentracion" class="text-sm text-secondary-600">
                      <span class="font-medium">Concentración:</span> {{ medicamento.concentracion }}
                    </p>
                  </div>
                  
                  <div class="text-right">
                    <p class="text-sm font-medium text-secondary-900">
                      Prescrito: {{ medicamento.cantidad_prescrita }} {{ medicamento.unidad_medida }}
                    </p>
                    <p v-if="medicamento.total_lotes_dispensados > 0" class="text-xs text-orange-600 font-medium">
                      Pendiente: {{ medicamento.cantidad_prescrita - (medicamento.total_lotes_dispensados || 0) }} {{ medicamento.unidad_medida }}
                    </p>
                    <p class="text-xs text-secondary-600">
                      {{ medicamento.dosis }}
                    </p>
                  </div>
                </div>

                <!-- Formulario de dispensación -->
                <div v-if="!medicamento.is_completely_dispensed" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
                  <div>
                    <label class="form-label">
                      Cantidad a Surtir *
                    </label>
                    <input
                      v-model.number="medicamento.cantidad_surtida"
                      type="number"
                      :max="medicamento.cantidad_prescrita - (medicamento.total_lotes_dispensados || 0)"
                      min="0"
                      class="form-input"
                      :class="{ 'border-accent-500': errors[`medicamento_${medicamento.id}_cantidad`] }"
                      @input="validateMedicamento(medicamento)"
                    />
                    <p v-if="errors[`medicamento_${medicamento.id}_cantidad`]" class="form-error">
                      {{ errors[`medicamento_${medicamento.id}_cantidad`] }}
                    </p>
                  </div>

                  <div>
                    <label class="form-label">
                      Lote *
                    </label>
                    <input
                      v-model="medicamento.lote"
                      type="text"
                      class="form-input"
                      :class="{ 'border-accent-500': errors[`medicamento_${medicamento.id}_lote`] }"
                      placeholder="Lote del medicamento"
                      @input="validateMedicamento(medicamento)"
                    />
                    <p v-if="errors[`medicamento_${medicamento.id}_lote`]" class="form-error">
                      {{ errors[`medicamento_${medicamento.id}_lote`] }}
                    </p>
                  </div>

                  <div>
                    <label class="form-label">
                      Fecha de Caducidad *
                    </label>
                    <input
                      v-model="medicamento.fecha_caducidad"
                      type="date"
                      class="form-input"
                      :class="{ 'border-accent-500': errors[`medicamento_${medicamento.id}_caducidad`] }"
                      @input="validateMedicamento(medicamento)"
                    />
                    <p v-if="errors[`medicamento_${medicamento.id}_caducidad`]" class="form-error">
                      {{ errors[`medicamento_${medicamento.id}_caducidad`] }}
                    </p>
                  </div>

                  <div>
                    <label class="form-label">
                      Laboratorio
                    </label>
                    <input
                      v-model="medicamento.laboratorio"
                      type="text"
                      class="form-input"
                      placeholder="Laboratorio fabricante"
                    />
                  </div>
                </div>

                <!-- Mensaje para medicamentos completamente dispensados -->
                <div v-else class="pt-4 border-t border-gray-200">
                  <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div class="flex items-center">
                      <svg class="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                      <div class="text-sm">
                        <p class="text-green-800 font-medium">Medicamento completamente dispensado</p>
                        <p class="text-green-700">Este medicamento ya ha sido dispensado en su totalidad y no se puede modificar.</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Observaciones específicas del medicamento -->
                <div v-if="!medicamento.is_completely_dispensed" class="mt-4">
                  <label class="form-label">
                    Observaciones
                  </label>
                  <textarea
                    v-model="medicamento.observaciones"
                    class="form-input"
                    rows="2"
                    placeholder="Observaciones específicas para este medicamento..."
                  ></textarea>
                </div>

                <!-- Indicador de progreso -->
                <div class="mt-4">
                  <div class="flex justify-between text-sm text-secondary-600 mb-1">
                    <span>Progreso de dispensación</span>
                    <span>{{ medicamento.total_lotes_dispensados || medicamento.cantidad_surtida || 0 }} / {{ medicamento.cantidad_prescrita }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      class="h-2 rounded-full transition-all duration-300"
                      :class="getProgressColor(medicamento)"
                      :style="{ width: getProgressPercentage(medicamento) + '%' }"
                    ></div>
                  </div>
                </div>

                <!-- Botón de gestión de lotes múltiples -->
                <div class="mt-4 flex justify-end">
                  <button
                    @click="abrirGestionLotes(medicamento)"
                    type="button"
                    :disabled="medicamento.is_completely_dispensed"
                    :class="[
                      'text-sm',
                      medicamento.is_completely_dispensed 
                        ? 'btn btn-disabled cursor-not-allowed opacity-50' 
                        : 'btn btn-outline'
                    ]"
                    :title="medicamento.is_completely_dispensed ? 'Este medicamento ya está completamente dispensado y no se puede modificar' : 'Gestionar lotes de este medicamento'"
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                    </svg>
                    {{ medicamento.is_completely_dispensed ? 'Completo' : 'Gestionar Lotes' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Observaciones generales -->
        <div class="card mt-6">
          <div class="card-body">
            <label class="form-label">
              Observaciones Generales de Dispensación
            </label>
            <textarea
              v-model="observacionesGenerales"
              class="form-input"
              rows="3"
              placeholder="Observaciones generales sobre la dispensación de esta receta..."
            ></textarea>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="flex justify-end space-x-4 pt-6 border-t border-gray-200 mt-6">
          <button
            type="button"
            @click="$emit('close')"
            class="btn-secondary"
          >
            Cancelar
          </button>
          
          <button
            @click="dispensarParcial"
            :disabled="!canDispenseParcial || isSubmitting"
            class="btn-primary"
          >
            Dispensar Parcial
          </button>
          
          <button
            @click="dispensarCompleta"
            :disabled="!canDispenseComplete || isSubmitting"
            class="btn-success"
          >
            <span v-if="isSubmitting">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Dispensando...
            </span>
            <span v-else>
              Dispensar Completa
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de gestión de lotes -->
    <GestionLotesMedicamento
      v-if="mostrarGestionLotes"
      :medicamento="medicamentoSeleccionado"
      :receta-id="recipe.folio_receta"
      @close="cerrarGestionLotes"
      @lote-agregado="onLoteAgregado"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import api from '@/services/api'
import {
  XMarkIcon
} from '@heroicons/vue/24/outline'
import GestionLotesMedicamento from './GestionLotesMedicamento.vue'

export default {
  name: 'DispensarReceta',
  components: {
    XMarkIcon,
    GestionLotesMedicamento
  },
  props: {
    recipe: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true,
      validator: value => ['FARMACIA', 'CMI'].includes(value)
    }
  },
  emits: ['close', 'dispensed', 'recetaActualizada'],
  setup(props, { emit }) {
    const toast = useToast()
    
    const medicamentos = ref([])
    const isLoading = ref(false)
    const isSubmitting = ref(false)
    const observacionesGenerales = ref('')
    const errors = reactive({})
    
    // Estado para gestión de lotes
    const mostrarGestionLotes = ref(false)
    const medicamentoSeleccionado = ref(null)
    
    // Función para limpiar estado
    const clearState = () => {
      medicamentos.value = []
      observacionesGenerales.value = ''
      Object.keys(errors).forEach(key => delete errors[key])
      mostrarGestionLotes.value = false
      medicamentoSeleccionado.value = null
      isLoading.value = false
      isSubmitting.value = false
    }
    
    const canDispenseParcial = computed(() => {
      return medicamentos.value.some(m => 
        m.cantidad_surtida > 0 && 
        m.lote && 
        m.fecha_caducidad &&
        !errors[`medicamento_${m.id}_cantidad`] &&
        !errors[`medicamento_${m.id}_lote`] &&
        !errors[`medicamento_${m.id}_caducidad`]
      )
    })
    
    const canDispenseComplete = computed(() => {
      return medicamentos.value.length > 0 && medicamentos.value.every(m => {
        // Verificar si el medicamento está completamente dispensado
        const cantidadDispensada = m.total_lotes_dispensados || m.cantidad_surtida || 0
        const estaCompleto = cantidadDispensada >= m.cantidad_prescrita
        
        // Si usa lotes múltiples (total_lotes_dispensados > 0), no necesita lote/fecha en el objeto principal
        const usaLotesMultiples = m.total_lotes_dispensados > 0
        
        if (usaLotesMultiples) {
          // Para lotes múltiples, solo verificar que esté completamente dispensado
          return estaCompleto && !errors[`medicamento_${m.id}_cantidad`]
        } else {
          // Para dispensación tradicional, verificar todos los campos
          return estaCompleto && 
                 m.lote && 
                 m.fecha_caducidad &&
                 !errors[`medicamento_${m.id}_cantidad`] &&
                 !errors[`medicamento_${m.id}_lote`] &&
                 !errors[`medicamento_${m.id}_caducidad`]
        }
      })
    })
    
    const loadMedicamentos = async () => {
      try {
        isLoading.value = true
        
        // Limpiar estado antes de cargar nuevos datos
        clearState()
        isLoading.value = true // Reestablecer después del clear
        
        console.log(`[DispensarReceta] Cargando medicamentos para receta #${props.recipe.folio_receta}`)
        
        const response = await api.get(`/recetas/${props.recipe.folio_receta}/`)
        const recetaCompleta = response.data
        
        console.log(`[DispensarReceta] Receta cargada:`, {
          folio: recetaCompleta.folio_receta,
          detalles: recetaCompleta.detalles?.length || 0,
          detallesIds: recetaCompleta.detalles?.map(d => d.id) || []
        })
        
        // Validar que los datos pertenecen a la receta correcta
        if (recetaCompleta.folio_receta !== props.recipe.folio_receta) {
          throw new Error(`Discrepancia de datos: esperaba receta #${props.recipe.folio_receta}, recibió #${recetaCompleta.folio_receta}`)
        }
        
        // Inicializar medicamentos con valores por defecto para dispensación
        medicamentos.value = recetaCompleta.detalles.map(detalle => ({
          ...detalle,
          cantidad_surtida: detalle.cantidad_surtida || 0,
          lote: detalle.lote || '',
          fecha_caducidad: detalle.fecha_caducidad || '',
          observaciones: detalle.observaciones_dispensacion || ''
        }))
        
        console.log(`[DispensarReceta] Medicamentos inicializados:`, medicamentos.value.length)
        
      } catch (error) {
        console.error('[DispensarReceta] Error loading medicamentos:', error)
        toast.error(`Error al cargar los medicamentos: ${error.message || 'Error desconocido'}`)
        clearState()
      } finally {
        isLoading.value = false
      }
    }
    
    const validateMedicamento = (medicamento) => {
      const baseKey = `medicamento_${medicamento.id}`
      
      // Limpiar errores previos
      delete errors[`${baseKey}_cantidad`]
      delete errors[`${baseKey}_lote`]
      delete errors[`${baseKey}_caducidad`]
      
      // Calcular cantidad pendiente considerando lotes ya dispensados
      const cantidadYaDispensada = medicamento.total_lotes_dispensados || 0
      const cantidadPendiente = medicamento.cantidad_prescrita - cantidadYaDispensada
      
      // Validar cantidad
      if (medicamento.cantidad_surtida < 0) {
        errors[`${baseKey}_cantidad`] = 'La cantidad no puede ser negativa'
      } else if (medicamento.cantidad_surtida > cantidadPendiente) {
        errors[`${baseKey}_cantidad`] = `Solo quedan ${cantidadPendiente} ${medicamento.unidad_medida || 'unidades'} por dispensar`
      } else if (medicamento.cantidad_surtida > medicamento.cantidad_prescrita) {
        errors[`${baseKey}_cantidad`] = 'No puede exceder la cantidad prescrita'
      }
      
      // Validar lote si hay cantidad a surtir
      if (medicamento.cantidad_surtida > 0 && !medicamento.lote.trim()) {
        errors[`${baseKey}_lote`] = 'El lote es requerido'
      }
      
      // Validar fecha de caducidad
      if (medicamento.cantidad_surtida > 0) {
        if (!medicamento.fecha_caducidad) {
          errors[`${baseKey}_caducidad`] = 'La fecha de caducidad es requerida'
        } else {
          const fechaCaducidad = new Date(medicamento.fecha_caducidad)
          const hoy = new Date()
          hoy.setHours(0, 0, 0, 0)
          
          if (fechaCaducidad <= hoy) {
            errors[`${baseKey}_caducidad`] = 'El medicamento no puede estar caducado'
          }
        }
      }
    }
    
    const validateAllMedicamentos = () => {
      medicamentos.value.forEach(validateMedicamento)
      return Object.keys(errors).length === 0
    }
    
    const dispensarParcial = async () => {
      if (!validateAllMedicamentos()) {
        toast.error('Por favor corrige los errores en el formulario')
        return
      }
      
      await procesarDispensacion(false)
    }
    
    const dispensarCompleta = async () => {
      if (!validateAllMedicamentos()) {
        toast.error('Por favor corrige los errores en el formulario')
        return
      }
      
      await procesarDispensacion(true)
    }
    
    const procesarDispensacion = async (esCompleta) => {
      try {
        isSubmitting.value = true
        
        // Actualizar cada medicamento
        const medicamentosADispenser = medicamentos.value.filter(m => m.cantidad_surtida > 0)
        
        console.log(`[DispensarReceta] Dispensando ${medicamentosADispenser.length} medicamentos:`, 
          medicamentosADispenser.map(m => ({ id: m.id, descripcion: m.descripcion_medicamento })))
        
        const promises = medicamentosADispenser.map(async (medicamento) => {
          console.log(`[DispensarReceta] Actualizando medicamento ID ${medicamento.id}`)
          
          try {
            const response = await api.patch(`/recetas/detalles/${medicamento.id}/`, {
              cantidad_surtida: medicamento.cantidad_surtida,
              lote: medicamento.lote,
              fecha_caducidad: medicamento.fecha_caducidad,
              observaciones_dispensacion: medicamento.observaciones || ''
            })
            console.log(`[DispensarReceta] Medicamento ID ${medicamento.id} actualizado exitosamente`)
            return response
          } catch (error) {
            console.error(`[DispensarReceta] Error actualizando medicamento ID ${medicamento.id}:`, error)
            throw error
          }
        })
        
        await Promise.all(promises)
        
        // El backend automáticamente actualiza el estado de la receta
        // cuando todos los medicamentos están completamente dispensados
        
        const message = esCompleta ? 'Receta dispensada completamente' : 'Dispensación parcial registrada'
        toast.success(message)
        
        emit('dispensed', {
          ...props.recipe,
          estado: esCompleta ? 'SURTIDA' : 'VALIDADA'
        })
        
      } catch (error) {
        console.error('Error dispensing recipe:', error)
        toast.error('Error al procesar la dispensación')
      } finally {
        isSubmitting.value = false
      }
    }
    
    const getPriorityClass = (priority) => {
      const classes = {
        'URGENTE': 'bg-accent-600 text-white',
        'ALTA': 'bg-orange-500 text-white',
        'MEDIA': 'bg-blue-500 text-white',
        'BAJA': 'bg-gray-500 text-white'
      }
      return classes[priority] || 'bg-gray-500 text-white'
    }
    
    const getProgressPercentage = (medicamento) => {
      if (!medicamento.cantidad_prescrita) return 0
      
      // Usar total de lotes dispensados si existen, sino usar cantidad_surtida tradicional
      const cantidadRealDispensada = medicamento.total_lotes_dispensados || medicamento.cantidad_surtida || 0
      
      return Math.min(100, (cantidadRealDispensada / medicamento.cantidad_prescrita) * 100)
    }
    
    const getProgressColor = (medicamento) => {
      const percentage = getProgressPercentage(medicamento)
      if (percentage === 100) return 'bg-success'
      if (percentage > 50) return 'bg-blue-500'
      if (percentage > 0) return 'bg-warning'
      return 'bg-gray-300'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return format(new Date(dateString), 'dd/MM/yyyy HH:mm', { locale: es })
    }
    
    // Funciones para gestión de lotes
    const abrirGestionLotes = (medicamento) => {
      medicamentoSeleccionado.value = medicamento
      mostrarGestionLotes.value = true
    }
    
    const cerrarGestionLotes = () => {
      mostrarGestionLotes.value = false
      medicamentoSeleccionado.value = null
    }
    
    const onLoteAgregado = async (datosLote) => {
      try {
        // Si tenemos los datos actualizados del medicamento, actualizarlos inmediatamente
        if (datosLote.medicamentoActualizado) {
          const medicamentoIndex = medicamentos.value.findIndex(m => m.id === datosLote.medicamentoActualizado.id)
          if (medicamentoIndex !== -1) {
            // Actualizar el medicamento específico en la lista
            medicamentos.value[medicamentoIndex] = {
              ...medicamentos.value[medicamentoIndex],
              ...datosLote.medicamentoActualizado
            }
          }
        }
        
        // Recargar los medicamentos para obtener los datos más recientes del servidor
        await loadMedicamentos()
        
        // También emitir evento al componente padre para que actualice la receta
        emit('recetaActualizada')
        
        toast.success('Lote agregado correctamente')
      } catch (error) {
        console.error('Error al procesar lote agregado:', error)
        // Intentar recargar de todos modos
        await loadMedicamentos()
        toast.success('Lote agregado correctamente')
      }
    }
    
    // Watcher para detectar cambios en la receta
    watch(
      () => props.recipe?.folio_receta,
      async (newFolio, oldFolio) => {
        if (newFolio && newFolio !== oldFolio) {
          console.log(`[DispensarReceta] Cambio de receta detectado: ${oldFolio} → ${newFolio}`)
          await nextTick()
          await loadMedicamentos()
        }
      },
      { immediate: false }
    )
    
    onMounted(() => {
      console.log(`[DispensarReceta] Componente montado para receta #${props.recipe?.folio_receta}`)
      loadMedicamentos()
    })
    
    return {
      medicamentos,
      isLoading,
      isSubmitting,
      observacionesGenerales,
      errors,
      canDispenseParcial,
      canDispenseComplete,
      validateMedicamento,
      dispensarParcial,
      dispensarCompleta,
      getPriorityClass,
      getProgressPercentage,
      getProgressColor,
      formatDate,
      // Gestión de lotes
      mostrarGestionLotes,
      medicamentoSeleccionado,
      abrirGestionLotes,
      cerrarGestionLotes,
      onLoteAgregado
    }
  }
}
</script>
