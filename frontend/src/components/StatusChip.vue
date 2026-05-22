<template>
  <v-chip :color="color" size="small" variant="tonal">{{ status }}</v-chip>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
  },
})

const color = computed(() => (props.status === 'Discharged' ? 'secondary' : 'success'))
</script>
