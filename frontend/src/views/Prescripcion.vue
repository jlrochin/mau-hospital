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
              Prescripción de Recetas
            </h1>
          </div>
          
          <div class="flex items-center space-x-4">
            <button
              @click="showCreateRecipe = true"
              class="btn-primary"
            >
              <PlusIcon class="h-5 w-5 mr-2" />
              Nueva Receta
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="scrollable-content p-6">
      <div class="max-w-7xl mx-auto">
        <!-- Barra de búsqueda de paciente -->
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

        <!-- Mensaje si no hay paciente seleccionado -->
        <div v-if="!selectedPatient" class="text-center py-12">
          <UserIcon class="mx-auto h-12 w-12 text-secondary-400" />
          <h3 class="mt-2 text-lg font-medium text-secondary-900">Selecciona un paciente</h3>
          <p class="mt-1 text-secondary-600">
            Busca y selecciona un paciente para crear una nueva receta.
          </p>
        </div>
      </div>
    </main>

    <!-- Modal para crear receta -->
    <FormularioReceta
      v-if="showCreateRecipe && selectedPatient"
      :patient="selectedPatient"
      @close="showCreateRecipe = false"
      @saved="onRecipeSaved"
    />

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
  PlusIcon,
  UserIcon
} from '@heroicons/vue/24/outline'

// Importar componentes
import BuscarPaciente from '@/components/atencion-usuario/BuscarPaciente.vue'
import DetallePaciente from '@/components/shared/DetallePaciente.vue'
import FormularioPaciente from '@/components/atencion-usuario/FormularioPaciente.vue'
import FormularioReceta from '@/components/shared/FormularioReceta.vue'
import HistorialPaciente from '@/components/shared/HistorialPaciente.vue'

export default {
  name: 'Prescripcion',
  components: {
    ArrowLeftIcon,
    PlusIcon,
    UserIcon,
    BuscarPaciente,
    DetallePaciente,
    FormularioPaciente,
    FormularioReceta,
    HistorialPaciente
  },
  setup() {
    const toast = useToast()
    
    const selectedPatient = ref(null)
    const showCreateRecipe = ref(false)
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
    
    const onRecipeSaved = (recipe) => {
      showCreateRecipe.value = false
      toast.success(`Receta #${recipe.folio_receta} creada correctamente`)
    }
    
    return {
      selectedPatient,
      showCreateRecipe,
      showCreatePatient,
      editingPatient,
      showHistory,
      onPatientSelected,
      onEditPatient,
      onViewHistory,
      closePatientModal,
      onPatientSaved,
      onRecipeSaved
    }
  }
}
</script>
