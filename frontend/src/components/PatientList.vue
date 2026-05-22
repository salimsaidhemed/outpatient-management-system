<template>
  <v-sheet class="panel" border>
    <div class="panel-header">
      <h2>Patient index</h2>
      <v-chip size="small" color="primary" variant="tonal">{{ patients.length }}</v-chip>
    </div>
    <div class="patient-list">
      <button
        v-for="patient in patients"
        :key="patient.id"
        class="patient-row"
        type="button"
        @click="$emit('select', patient)"
      >
        <span>
          <strong>{{ patient.fullName }}</strong>
          <small>{{ patient.mrn }} · {{ patient.age }} yrs · {{ patient.phone }}</small>
        </span>
        <v-icon icon="mdi-chevron-right" />
      </button>
      <v-empty-state
        v-if="!patients.length"
        icon="mdi-account-search"
        text="Registered patients will appear here."
        title="No patients"
      />
    </div>
  </v-sheet>
</template>

<script setup>
defineProps({
  patients: {
    type: Array,
    required: true,
  },
})

defineEmits(['select'])
</script>
