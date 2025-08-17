<template>
  <div class="space-y-4">
    <div class="flex space-x-4">
      <div class="flex-1">
        <label class="form-label">
          Buscar Paciente
        </label>
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            class="form-input pl-10"
            placeholder="Buscar por expediente, CURP o nombre..."
            @input="onSearchInput"
            @keydown.enter="performSearch"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon class="h-5 w-5 text-secondary-400" />
          </div>
        </div>
      </div>
      
      <div class="flex items-end space-x-2">
        <button
          @click="performSearch"
          :disabled="!searchQuery.trim() || isLoading"
          class="btn-primary"
        >
          <MagnifyingGlassIcon class="h-5 w-5 mr-2" />
          Buscar
        </button>
        
        <button
          @click="$emit('new-patient')"
          class="btn-secondary"
        >
          <PlusIcon class="h-5 w-5 mr-2" />
          Nuevo
        </button>
      </div>
    </div>

    <!-- Indicador de carga -->
    <div v-if="isLoading" class="text-center py-4">
      <div class="inline-flex items-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Buscando pacientes...
      </div>
    </div>

    <!-- Resultados de búsqueda -->
    <div v-if="searchResults.length > 0 && !isLoading" class="space-y-2">
      <h3 class="text-lg font-medium text-secondary-900">
        Resultados de búsqueda ({{ searchResults.length }})
      </h3>
      
      <div class="max-h-96 overflow-y-auto custom-scrollbar space-y-2">
        <div
          v-for="patient in searchResults"
          :key="patient.expediente"
          @click="selectPatient(patient)"
          class="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors duration-200"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="mb-2">
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-1">
                  <div>
                    <span class="text-xs font-medium text-secondary-500">Nombre(s):</span>
                    <p class="font-medium text-secondary-900">{{ patient.nombre }}</p>
                  </div>
                  <div>
                    <span class="text-xs font-medium text-secondary-500">Apellido Paterno:</span>
                    <p class="font-medium text-secondary-900">{{ patient.apellido_paterno }}</p>
                  </div>
                  <div>
                    <span class="text-xs font-medium text-secondary-500">Apellido Materno:</span>
                    <p class="font-medium text-secondary-900">{{ patient.apellido_materno || 'N/A' }}</p>
                  </div>
                </div>
              </div>
              <div class="mt-2 text-sm text-secondary-600 space-y-1">
                <p><span class="font-medium">Expediente:</span> {{ patient.expediente }}</p>
                <p><span class="font-medium">CURP:</span> {{ patient.curp }}</p>
                <p><span class="font-medium">Edad:</span> {{ patient.edad }} años</p>
                <p><span class="font-medium">Patología:</span> {{ patient.patologia }}</p>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <span class="badge bg-primary-600 text-white">
                {{ patient.genero }}
              </span>
              <ChevronRightIcon class="h-5 w-5 text-secondary-400" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensaje cuando no hay resultados -->
    <div v-if="showNoResults && !isLoading" class="text-center py-8">
      <ExclamationTriangleIcon class="mx-auto h-12 w-12 text-secondary-400" />
      <h3 class="mt-2 text-lg font-medium text-secondary-900">No se encontraron pacientes</h3>
      <p class="mt-1 text-secondary-600">
        No hay pacientes que coincidan con tu búsqueda.
      </p>
      <button
        @click="$emit('new-patient')"
        class="mt-4 btn-primary"
      >
        Crear nuevo paciente
      </button>
    </div>

    <!-- Duplicados encontrados (solo en modo verificación) -->
    <div v-if="duplicates.length > 0" class="bg-warning bg-opacity-10 border border-warning rounded-lg p-4">
      <div class="flex">
        <ExclamationTriangleIcon class="h-5 w-5 text-warning" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-warning">
            Pacientes duplicados encontrados
          </h3>
          <div class="mt-2 text-sm text-warning">
            <p>Se encontraron pacientes con información similar:</p>
            <ul class="mt-1 list-disc list-inside">
              <li v-for="duplicate in duplicates" :key="duplicate.paciente.expediente">
                {{ duplicate.paciente.nombre }} {{ duplicate.paciente.apellido_paterno }} {{ duplicate.paciente.apellido_materno || '' }} 
                ({{ duplicate.campo.toUpperCase() }}: {{ duplicate.valor }})
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import api from '@/services/api'
import {
  MagnifyingGlassIcon,
  PlusIcon,
  ChevronRightIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'BuscarPaciente',
  components: {
    MagnifyingGlassIcon,
    PlusIcon,
    ChevronRightIcon,
    ExclamationTriangleIcon
  },
  emits: ['patient-selected', 'new-patient'],
  setup(props, { emit }) {
    const toast = useToast()
    
    const searchQuery = ref('')
    const searchResults = ref([])
    const duplicates = ref([])
    const isLoading = ref(false)
    const hasSearched = ref(false)
    
    const showNoResults = computed(() => {
      return hasSearched.value && searchResults.value.length === 0 && searchQuery.value.trim()
    })
    
    let searchTimeout = null
    
    const onSearchInput = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(performSearch, 500)
    }
    
    const performSearch = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        hasSearched.value = false
        return
      }
      
      try {
        isLoading.value = true
        const response = await api.get('/pacientes/buscar/', {
          params: { q: searchQuery.value.trim() }
        })
        
        searchResults.value = response.data.results
        hasSearched.value = true
        
        if (searchResults.value.length === 0) {
          toast.info('No se encontraron pacientes con esos criterios')
        }
      } catch (error) {
        console.error('Error searching patients:', error)
        toast.error('Error al buscar pacientes')
        searchResults.value = []
      } finally {
        isLoading.value = false
      }
    }
    
    const selectPatient = (patient) => {
      emit('patient-selected', patient)
      const nombreCompleto = `${patient.nombre} ${patient.apellido_paterno} ${patient.apellido_materno || ''}`.trim()
      toast.success(`Paciente seleccionado: ${nombreCompleto}`)
    }
    
    // Método para verificar duplicados (usado desde componentes padre)
    const checkDuplicates = async (expediente, curp) => {
      try {
        const response = await api.get('/pacientes/verificar-duplicados/', {
          params: { expediente, curp }
        })
        
        duplicates.value = response.data.duplicados || []
        return response.data.duplicados_encontrados
      } catch (error) {
        console.error('Error checking duplicates:', error)
        return false
      }
    }
    
    const clearSearch = () => {
      searchQuery.value = ''
      searchResults.value = []
      duplicates.value = []
      hasSearched.value = false
    }
    
    return {
      searchQuery,
      searchResults,
      duplicates,
      isLoading,
      showNoResults,
      onSearchInput,
      performSearch,
      selectPatient,
      checkDuplicates,
      clearSearch
    }
  }
}
</script>
