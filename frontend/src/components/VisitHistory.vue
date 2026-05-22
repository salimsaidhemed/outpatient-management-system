<template>
  <v-sheet class="panel" border>
    <div class="panel-header">
      <h2>{{ selectedPatient ? `${selectedPatient.fullName} visits` : 'Visit history' }}</h2>
      <v-chip v-if="selectedPatient" size="small" color="secondary" variant="tonal">
        {{ selectedPatient.mrn }}
      </v-chip>
    </div>
    <v-timeline v-if="visits.length" density="compact" side="end">
      <v-timeline-item
        v-for="visit in visits"
        :key="visit.id"
        dot-color="primary"
        size="small"
      >
        <div class="visit-item">
          <strong>{{ visit.department }} · {{ visit.visitType }}</strong>
          <span>{{ visit.provider }} · {{ formatDate(visit.admittedAt) }}</span>
          <p>{{ visit.chiefComplaint }}</p>
          <StatusChip :status="visit.status" />
        </div>
      </v-timeline-item>
    </v-timeline>
    <v-empty-state
      v-else
      icon="mdi-history"
      text="Select a patient to review their outpatient visits."
      title="No visit selected"
    />
  </v-sheet>
</template>

<script setup>
import StatusChip from './StatusChip.vue'

defineProps({
  selectedPatient: {
    type: Object,
    default: null,
  },
  visits: {
    type: Array,
    required: true,
  },
})

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}
</script>
