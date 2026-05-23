<template>
  <section class="stack">
    <v-sheet v-if="selectedPatient" class="panel" border>
      <div class="panel-header">
        <div>
          <h2>{{ selectedPatient.fullName }}</h2>
          <p class="panel-subtitle">{{ selectedPatient.mrn }} · {{ selectedPatient.age }} yrs · {{ selectedPatient.sex }}</p>
        </div>
        <div class="detail-actions">
          <v-btn variant="tonal" color="secondary" prepend-icon="mdi-arrow-left" :to="{ name: 'patients' }">
            Patients
          </v-btn>
          <v-btn color="primary" prepend-icon="mdi-clipboard-plus" :to="{ name: 'admit' }">
            Admit
          </v-btn>
        </div>
      </div>

      <div class="patient-detail-grid">
        <v-sheet class="detail-item" border>
          <span>Date of birth</span>
          <strong>{{ selectedPatient.dateOfBirth }}</strong>
        </v-sheet>
        <v-sheet class="detail-item" border>
          <span>Phone</span>
          <strong>{{ selectedPatient.phone }}</strong>
        </v-sheet>
        <v-sheet class="detail-item" border>
          <span>Email</span>
          <strong>{{ selectedPatient.email || 'Not recorded' }}</strong>
        </v-sheet>
        <v-sheet class="detail-item" border>
          <span>Emergency contact</span>
          <strong>{{ selectedPatient.emergencyContact || 'Not recorded' }}</strong>
        </v-sheet>
        <v-sheet class="detail-item wide" border>
          <span>Address</span>
          <strong>{{ selectedPatient.address }}</strong>
        </v-sheet>
      </div>
    </v-sheet>

    <v-sheet v-else class="panel" border>
      <v-empty-state icon="mdi-account-search" title="Patient not found" text="Search for a patient to open their details." />
    </v-sheet>

    <VisitHistory :selected-patient="selectedPatient" :visits="selectedVisits" />
  </section>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import VisitHistory from '../components/VisitHistory.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const route = useRoute()
const { loadPatientDetail, selectedPatient, selectedVisits } = useAdmissionsStore()

async function loadCurrentPatient() {
  await loadPatientDetail(route.params.patientId)
}

onMounted(loadCurrentPatient)
watch(() => route.params.patientId, loadCurrentPatient)
</script>
