<template>
  <div class="relative">
    <!-- Campo de entrada con búsqueda -->
    <div class="relative">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showDropdown = true"
        @blur="handleBlur"
        type="text"
        :placeholder="placeholder || 'Buscar código CIE-10...'"
        class="w-full px-3 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-600 focus:border-primary-600 transition-colors"
        :class="{ 'border-accent-500': hasError }"
      />
      
      <!-- Icono de búsqueda -->
      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-secondary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
    </div>

    <!-- Dropdown de resultados -->
    <div
      v-if="showDropdown && (filteredCodes.length > 0 || isLoading)"
      class="absolute z-50 w-full mt-1 bg-white border border-secondary-300 rounded-lg shadow-lg max-h-60 overflow-y-auto"
    >
      <!-- Estado de carga -->
      <div v-if="isLoading" class="p-4 text-center text-secondary-600">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-2">Buscando códigos...</p>
      </div>

      <!-- Resultados -->
      <div v-else>
        <div
          v-for="code in filteredCodes"
          :key="code.codigo"
          @click="selectCode(code)"
          class="px-4 py-3 hover:bg-secondary-50 cursor-pointer border-b border-secondary-100 last:border-b-0 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <span class="font-mono text-sm font-bold text-primary-600 bg-primary-50 px-2 py-1 rounded">
                  {{ code.codigo }}
                </span>
                <span class="text-xs text-secondary-500 bg-secondary-100 px-2 py-1 rounded">
                  Cap. {{ code.capitulo }}
                </span>
              </div>
              <p class="text-sm font-medium text-secondary-900 mt-1">
                {{ code.descripcion_corta }}
              </p>
              <p class="text-xs text-secondary-600 mt-1 line-clamp-2">
                {{ code.descripcion }}
              </p>
            </div>
            
            <!-- Indicadores adicionales -->
            <div class="flex flex-col items-end space-y-1 ml-2">
              <span v-if="code.genero_aplicable !== 'AMBOS'" 
                    class="text-xs px-2 py-1 rounded text-white"
                    :class="code.genero_aplicable === 'MASCULINO' ? 'bg-blue-500' : 'bg-pink-500'">
                {{ code.genero_aplicable === 'MASCULINO' ? '♂' : '♀' }}
              </span>
              <span v-if="code.es_mortalidad" 
                    class="text-xs px-2 py-1 rounded bg-red-100 text-red-700">
                Mortalidad
              </span>
            </div>
          </div>
        </div>

        <!-- Sin resultados -->
        <div v-if="filteredCodes.length === 0 && searchQuery" 
             class="px-4 py-3 text-center text-secondary-500">
          <p>No se encontraron códigos CIE-10</p>
          <p class="text-sm">Intenta con otros términos de búsqueda</p>
        </div>
      </div>
    </div>

    <!-- Código seleccionado -->
    <div v-if="selectedCode" class="mt-3 p-3 bg-primary-50 border border-primary-200 rounded-lg">
      <div class="flex items-start justify-between">
        <div class="flex-1">
          <div class="flex items-center space-x-2 mb-2">
            <span class="font-mono text-lg font-bold text-primary-700 bg-white px-3 py-1 rounded border">
              {{ selectedCode.codigo }}
            </span>
            <span class="text-sm text-primary-600 bg-white px-2 py-1 rounded border">
              Capítulo {{ selectedCode.capitulo }}
            </span>
          </div>
          <h4 class="font-medium text-primary-900 mb-1">
            {{ selectedCode.descripcion_corta }}
          </h4>
          <p class="text-sm text-primary-700">
            {{ selectedCode.descripcion }}
          </p>
        </div>
        
        <!-- Botón para cambiar -->
        <button
          @click="clearSelection"
          type="button"
          class="ml-3 text-primary-600 hover:text-primary-800 transition-colors"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Información adicional -->
      <div class="mt-3 pt-3 border-t border-primary-200">
        <div class="grid grid-cols-2 gap-4 text-xs">
          <div>
            <span class="font-medium text-primary-700">Tipo:</span>
            <span class="ml-1 text-primary-600">{{ getTipoDisplay(selectedCode.tipo) }}</span>
          </div>
          <div>
            <span class="font-medium text-primary-700">Género:</span>
            <span class="ml-1 text-primary-600">{{ getGeneroDisplay(selectedCode.genero_aplicable) }}</span>
          </div>
          <div v-if="selectedCode.edad_minima || selectedCode.edad_maxima">
            <span class="font-medium text-primary-700">Edad:</span>
            <span class="ml-1 text-primary-600">
              {{ selectedCode.edad_minima || '0' }} - {{ selectedCode.edad_maxima || '∞' }} años
            </span>
          </div>
          <div>
            <span class="font-medium text-primary-700">Aplicabilidad:</span>
            <span class="ml-1 text-primary-600">
              {{ selectedCode.es_morbilidad ? 'Morbilidad' : '' }}{{ selectedCode.es_mortalidad && selectedCode.es_morbilidad ? ', ' : '' }}{{ selectedCode.es_mortalidad ? 'Mortalidad' : '' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensaje de error -->
    <p v-if="hasError" class="mt-1 text-sm text-accent-500">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

export default {
  name: 'SelectorCIE10',
  props: {
    modelValue: {
      type: [String, Object],
      default: ''
    },
    placeholder: {
      type: String,
      default: 'Buscar código CIE-10...'
    },
    required: {
      type: Boolean,
      default: false
    },
    errorMessage: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue', 'code-selected'],
  setup(props, { emit }) {
    const toast = useToast()
    
    const searchQuery = ref('')
    const showDropdown = ref(false)
    const isLoading = ref(false)
    const filteredCodes = ref([])
    const selectedCode = ref(null)
    const searchTimeout = ref(null)

    // Computed properties
    const hasError = computed(() => props.errorMessage && props.errorMessage.length > 0)

    // Métodos
    const handleSearch = () => {
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value)
      }
      
      searchTimeout.value = setTimeout(() => {
        if (searchQuery.value.trim().length >= 2) {
          searchCodes()
        } else {
          filteredCodes.value = []
        }
      }, 300)
    }

    const searchCodes = async () => {
      if (!searchQuery.value.trim()) return
      
      isLoading.value = true
      try {
        const response = await api.get(`/pacientes/cie10/buscar/?q=${encodeURIComponent(searchQuery.value.trim())}`)
        filteredCodes.value = response.data.results || []
      } catch (error) {
        console.error('Error buscando códigos CIE-10:', error)
        toast.error('Error al buscar códigos CIE-10')
        filteredCodes.value = []
      } finally {
        isLoading.value = false
      }
    }

    const selectCode = (code) => {
      selectedCode.value = code
      searchQuery.value = code.codigo
      showDropdown.value = false
      emit('update:modelValue', code.codigo)
      emit('code-selected', code)
      toast.success(`Código CIE-10 seleccionado: ${code.codigo}`)
    }

    const clearSelection = () => {
      selectedCode.value = null
      searchQuery.value = ''
      emit('update:modelValue', '')
      emit('code-selected', null)
    }

    const handleBlur = () => {
      // Pequeño delay para permitir que se ejecute el click en los resultados
      setTimeout(() => {
        showDropdown.value = false
      }, 150)
    }

    const getTipoDisplay = (tipo) => {
      const tipos = {
        'ENFERMEDAD': 'Enfermedad',
        'TRAUMATISMO': 'Traumatismo',
        'FACTOR_EXTERNO': 'Causa externa',
        'FACTOR_SALUD': 'Factor de salud'
      }
      return tipos[tipo] || tipo
    }

    const getGeneroDisplay = (genero) => {
      const generos = {
        'AMBOS': 'Ambos géneros',
        'MASCULINO': 'Solo masculino',
        'FEMENINO': 'Solo femenino'
      }
      return generos[genero] || genero
    }

    // Inicializar con valor existente
    const initializeWithValue = async () => {
      if (props.modelValue && typeof props.modelValue === 'string') {
        try {
          // Buscar el código en el catálogo
          const response = await api.get(`/pacientes/cie10/buscar/?q=${props.modelValue}`)
          const codes = response.data.results || []
          const foundCode = codes.find(code => code.codigo === props.modelValue)
          if (foundCode) {
            selectedCode.value = foundCode
            searchQuery.value = foundCode.codigo
          }
        } catch (error) {
          console.error('Error inicializando código CIE-10:', error)
        }
      }
    }

    // Watchers
    watch(() => props.modelValue, (newValue) => {
      if (newValue && !selectedCode.value) {
        initializeWithValue()
      }
    })

    // Lifecycle
    onMounted(() => {
      if (props.modelValue) {
        initializeWithValue()
      }
    })

    return {
      searchQuery,
      showDropdown,
      isLoading,
      filteredCodes,
      selectedCode,
      hasError,
      handleSearch,
      selectCode,
      clearSelection,
      handleBlur,
      getTipoDisplay,
      getGeneroDisplay
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
