<template>
  <div id="app" class="min-h-screen bg-background-main">
    <!-- Loading spinner mientras se inicializa la autenticación -->
    <div v-if="isInitializing" class="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
        <p class="text-secondary-600">Inicializando aplicación...</p>
      </div>
    </div>
    
    <!-- Contenido principal -->
    <router-view v-else />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const toast = useToast()
    const isInitializing = ref(true)

    const initializeApp = async () => {
      try {
        await authStore.initializeAuth()
      } catch (error) {
        console.error('Error initializing auth:', error)
        // No mostrar error si no hay token (usuario no logueado)
        if (authStore.tokens.access) {
          toast.error('Error al inicializar la sesión')
        }
      } finally {
        isInitializing.value = false
      }
    }

    onMounted(() => {
      initializeApp()
    })

    return {
      isInitializing
    }
  }
}
</script>
