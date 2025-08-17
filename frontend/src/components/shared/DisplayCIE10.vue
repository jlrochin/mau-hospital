<template>
  <div v-if="code" class="inline-flex items-center space-x-2">
    <!-- Código CIE-10 -->
    <span class="font-mono text-sm font-bold text-primary-600 bg-primary-50 px-2 py-1 rounded border">
      {{ code.codigo }}
    </span>
    
    <!-- Descripción corta -->
    <span class="text-sm text-secondary-700">
      {{ code.descripcion_corta }}
    </span>
    
    <!-- Indicadores adicionales -->
    <div class="flex items-center space-x-1">
      <span v-if="code.genero_aplicable !== 'AMBOS'" 
            class="text-xs px-1.5 py-0.5 rounded text-white text-xs"
            :class="code.genero_aplicable === 'MASCULINO' ? 'bg-blue-500' : 'bg-pink-500'">
        {{ code.genero_aplicable === 'MASCULINO' ? '♂' : '♀' }}
      </span>
      
      <span v-if="code.es_mortalidad" 
            class="text-xs px-1.5 py-0.5 rounded bg-red-100 text-red-700">
        Mortalidad
      </span>
      
      <span v-if="code.capitulo" 
            class="text-xs px-1.5 py-0.5 rounded bg-secondary-100 text-secondary-600">
        Cap. {{ code.capitulo }}
      </span>
    </div>
  </div>
  
  <!-- Estado cuando no hay código -->
  <div v-else class="text-sm text-secondary-500 italic">
    No especificado
  </div>
</template>

<script>
export default {
  name: 'DisplayCIE10',
  props: {
    code: {
      type: Object,
      default: null
    }
  }
}
</script>
