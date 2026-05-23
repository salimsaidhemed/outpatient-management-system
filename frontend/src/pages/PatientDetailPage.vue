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
          <v-btn variant="tonal" color="primary" prepend-icon="mdi-pencil" @click="preparePatientEdit()">
            Edit
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

    <v-dialog v-model="editingPatient" max-width="760">
      <v-sheet class="panel" border>
        <div class="panel-header">
          <div>
            <h2>Edit patient</h2>
            <p class="panel-subtitle">Update demographic and contact details for this patient record.</p>
          </div>
          <v-btn icon="mdi-close" variant="text" @click="editingPatient = false" />
        </div>

        <v-form @submit.prevent="savePatientEdit">
          <div class="two-column">
            <v-text-field v-model="patientEditForm.firstName" label="First name" required />
            <v-text-field v-model="patientEditForm.lastName" label="Last name" required />
            <v-text-field v-model="patientEditForm.dateOfBirth" label="Date of birth" type="date" required />
            <v-select v-model="patientEditForm.sex" :items="sexOptions" label="Sex" required />
            <v-text-field v-model="patientEditForm.phone" label="Phone" required />
            <v-text-field v-model="patientEditForm.email" label="Email" type="email" />
          </div>
          <v-textarea v-model="patientEditForm.address" label="Address" rows="2" required />
          <v-text-field v-model="patientEditForm.emergencyContact" label="Emergency contact" />
          <div class="actions">
            <v-btn variant="text" @click="editingPatient = false">Cancel</v-btn>
            <v-btn color="primary" prepend-icon="mdi-content-save" type="submit" :loading="savingPatientEdit">
              Save changes
            </v-btn>
          </div>
        </v-form>
      </v-sheet>
    </v-dialog>
  </section>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

import VisitHistory from '../components/VisitHistory.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const route = useRoute()
const {
  editingPatient,
  loadPatientDetail,
  patientEditForm,
  preparePatientEdit,
  savePatientEdit,
  savingPatientEdit,
  selectedPatient,
  selectedVisits,
  sexOptions,
} = useAdmissionsStore()

async function loadCurrentPatient() {
  await loadPatientDetail(route.params.patientId)
}

onMounted(loadCurrentPatient)
watch(() => route.params.patientId, loadCurrentPatient)
</script>
