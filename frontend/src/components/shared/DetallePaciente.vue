<template>
  <div class="card">
    <div class="card-header">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold text-secondary-900">
          Información del Paciente
        </h2>
        <div class="flex space-x-2">
          <button
            @click="$emit('edit-patient', patient)"
            class="btn-secondary text-sm"
          >
            <PencilIcon class="h-4 w-4 mr-1" />
            Editar
          </button>
          <button
            @click="$emit('view-history')"
            class="btn-primary text-sm"
          >
            <ClockIcon class="h-4 w-4 mr-1" />
            Historial
          </button>
        </div>
      </div>
    </div>
    
    <div class="card-body">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Información básica -->
        <div class="space-y-3">
          <h3 class="text-lg font-medium text-secondary-900 border-b border-gray-200 pb-2">
            Información Básica
          </h3>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Expediente:</span>
              <span class="text-secondary-900">{{ patient.expediente }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">CURP:</span>
              <span class="text-secondary-900">{{ patient.curp }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Nombre(s):</span>
              <span class="text-secondary-900">{{ patient.nombre }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Apellido Paterno:</span>
              <span class="text-secondary-900">{{ patient.apellido_paterno }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Apellido Materno:</span>
              <span class="text-secondary-900">{{ patient.apellido_materno || 'No especificado' }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Edad:</span>
              <span class="text-secondary-900">{{ patient.edad }} años</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Género:</span>
              <span class="badge bg-primary-600 text-white">
                {{ getGenderDisplay(patient.genero) }}
              </span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Tipo de Sangre:</span>
              <span class="badge bg-accent-600 text-white">
                {{ getBloodTypeDisplay(patient.tipo_sangre) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Información médica -->
        <div class="space-y-3">
          <h3 class="text-lg font-medium text-secondary-900 border-b border-gray-200 pb-2">
            Información Médica
          </h3>
          
          <div class="space-y-2 text-sm">
            <div>
              <span class="font-medium text-secondary-600">Patología:</span>
              <p class="text-secondary-900 mt-1 break-words">
                {{ patient.patologia || 'No especificado' }}
              </p>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">CIE-10:</span>
              <span class="text-secondary-900">
                {{ patient.cie10 || 'No especificado' }}
              </span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Fecha Diagnóstico:</span>
              <span class="text-secondary-900">
                {{ formatDate(patient.fecha_diagnostico) || 'No especificado' }}
              </span>
            </div>
            
            <div v-if="patient.alergias">
              <span class="font-medium text-secondary-600">Alergias:</span>
              <p class="text-secondary-900 mt-1 bg-orange-50 p-2 rounded text-xs border border-orange-200">
                {{ patient.alergias }}
              </p>
            </div>
          </div>
        </div>

        <!-- Información de contacto -->
        <div class="space-y-3">
          <h3 class="text-lg font-medium text-secondary-900 border-b border-gray-200 pb-2">
            Contacto y Seguro
          </h3>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Teléfono:</span>
              <span class="text-secondary-900">{{ patient.telefono || 'No especificado' }}</span>
            </div>
            
            <div>
              <span class="font-medium text-secondary-600">Dirección:</span>
              <p class="text-secondary-900 mt-1 break-words">
                {{ patient.direccion || 'No especificado' }}
              </p>
            </div>
            
            <div>
              <span class="font-medium text-secondary-600">Contacto Emergencia:</span>
              <p class="text-secondary-900 mt-1">
                {{ patient.contacto_emergencia_nombre || 'No especificado' }}
                <span v-if="patient.contacto_emergencia_telefono" class="block text-xs text-secondary-600">
                  {{ patient.contacto_emergencia_telefono }}
                </span>
              </p>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">NSS:</span>
              <span class="text-secondary-900">{{ patient.numero_seguro_social || 'No especificado' }}</span>
            </div>
            
            <div class="flex justify-between">
              <span class="font-medium text-secondary-600">Institución:</span>
              <span class="badge bg-blue-500 text-white">
                {{ patient.institucion_seguro || 'No especificado' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado del paciente -->
      <div class="mt-6 pt-4 border-t border-gray-200">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between text-sm text-secondary-600 space-y-2 sm:space-y-0">
          <div class="flex flex-col sm:flex-row sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
            <span class="flex items-center">
              <span class="font-medium">Estado:</span>
              <span
                class="ml-2 badge"
                :class="patient.is_active ? 'bg-success text-white' : 'bg-gray-500 text-white'"
              >
                {{ patient.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </span>
            
            <span>
              <span class="font-medium">Registrado:</span>
              {{ formatDate(patient.created_at) || 'No disponible' }}
            </span>
          </div>
          
          <div v-if="patient.updated_at && patient.updated_at !== patient.created_at" class="text-right">
            <span class="font-medium">Última actualización:</span>
            {{ formatDate(patient.updated_at) || 'No disponible' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { format } from 'date-fns'
import { es } from 'date-fns/locale'
import {
  PencilIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'DetallePaciente',
  components: {
    PencilIcon,
    ClockIcon
  },
  props: {
    patient: {
      type: Object,
      required: true
    }
  },
  emits: ['edit-patient', 'view-history'],
  setup() {
    const getGenderDisplay = (gender) => {
      const genders = {
        'M': 'Masculino',
        'F': 'Femenino',
        'O': 'Otro'
      }
      return genders[gender] || gender || 'No especificado'
    }
    
    const getBloodTypeDisplay = (bloodType) => {
      const bloodTypes = {
        'A+': 'A+', 'A-': 'A-',
        'B+': 'B+', 'B-': 'B-',
        'AB+': 'AB+', 'AB-': 'AB-',
        'O+': 'O+', 'O-': 'O-',
        'ND': 'No Determinado'
      }
      return bloodTypes[bloodType] || bloodType || 'No Determinado'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return null
      
      try {
        const date = new Date(dateString)
        if (isNaN(date.getTime())) return null
        return format(date, 'dd/MM/yyyy', { locale: es })
      } catch (error) {
        return null
      }
    }
    
    return {
      getGenderDisplay,
      getBloodTypeDisplay,
      formatDate
    }
  }
}
</script>
