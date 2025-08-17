<template>
  <div class="min-h-screen bg-background-main">
    <!-- Header sticky -->
    <header class="sticky-header">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <router-link to="/" class="text-secondary-600 hover:text-primary-600">
              <ArrowLeftIcon class="h-6 w-6" />
            </router-link>
            <h1 class="text-xl font-bold text-secondary-900">
              Atención al Usuario
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <button
              @click="showCreatePatient = true"
              class="btn-primary"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              Nuevo Paciente
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="scrollable-content p-6">
      <div class="max-w-7xl mx-auto">
        <!-- Barra de búsqueda -->
        <div class="card mb-6">
          <div class="card-body">
            <BuscarPaciente 
              @patient-selected="onPatientSelected"
              @new-patient="showCreatePatient = true"
            />
          </div>
        </div>

        <!-- Información del paciente seleccionado -->
        <div v-if="selectedPatient" class="mb-6">
          <DetallePaciente 
            :patient="selectedPatient"
            @edit-patient="onEditPatient"
            @view-history="onViewHistory"
          />
        </div>

        <!-- Cola de validación -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-xl font-bold text-secondary-900">
              Cola de Validación de Recetas
            </h2>
            <p class="text-sm text-secondary-600 mt-1">
              Recetas pendientes de validación
            </p>
          </div>
          <div class="card-body">
            <ColaValidacion 
              @recipe-validated="onRecipeValidated"
            />
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para crear/editar paciente -->
    <FormularioPaciente
      v-if="showCreatePatient || editingPatient"
      :patient="editingPatient"
      @close="closePatientModal"
      @saved="onPatientSaved"
    />

    <!-- Modal para historial del paciente -->
    <HistorialPaciente
      v-if="showHistory && selectedPatient"
      :patient="selectedPatient"
      @close="showHistory = false"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import {
  ArrowLeftIcon,
  PlusIcon
} from '@heroicons/vue/24/outline'

// Importar componentes
import BuscarPaciente from '@/components/atencion-usuario/BuscarPaciente.vue'
import DetallePaciente from '@/components/shared/DetallePaciente.vue'
import FormularioPaciente from '@/components/atencion-usuario/FormularioPaciente.vue'
import ColaValidacion from '@/components/atencion-usuario/ColaValidacion.vue'
import HistorialPaciente from '@/components/shared/HistorialPaciente.vue'

export default {
  name: 'AtencionUsuario',
  components: {
    ArrowLeftIcon,
    PlusIcon,
    BuscarPaciente,
    DetallePaciente,
    FormularioPaciente,
    ColaValidacion,
    HistorialPaciente
  },
  setup() {
    const toast = useToast()
    
    const selectedPatient = ref(null)
    const showCreatePatient = ref(false)
    const editingPatient = ref(null)
    const showHistory = ref(false)
    
    const onPatientSelected = (patient) => {
      selectedPatient.value = patient
    }
    
    const onEditPatient = (patient) => {
      editingPatient.value = patient
    }
    
    const onViewHistory = () => {
      showHistory.value = true
    }
    
    const closePatientModal = () => {
      showCreatePatient.value = false
      editingPatient.value = null
    }
    
    const onPatientSaved = (patient) => {
      selectedPatient.value = patient
      closePatientModal()
      toast.success('Paciente guardado correctamente')
    }
    
    const onRecipeValidated = () => {
      toast.success('Receta validada correctamente')
    }
    
    return {
      selectedPatient,
      showCreatePatient,
      editingPatient,
      showHistory,
      onPatientSelected,
      onEditPatient,
      onViewHistory,
      closePatientModal,
      onPatientSaved,
      onRecipeValidated
    }
  }
}
</script>
