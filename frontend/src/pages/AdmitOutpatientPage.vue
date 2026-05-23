<template>
  <section class="form-grid">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <h2>New outpatient admission</h2>
      </div>
      <v-form @submit.prevent="submitAdmission">
        <v-autocomplete
          v-model="admissionForm.patientId"
          :items="patientOptions"
          item-title="label"
          item-value="id"
          label="Patient"
          prepend-inner-icon="mdi-account-search"
          required
        />
        <div class="two-column">
          <v-select v-model="admissionForm.department" :items="departments" label="Department" required />
          <v-text-field v-model="admissionForm.provider" label="Provider" required />
          <v-select v-model="admissionForm.visitType" :items="visitTypes" label="Visit type" required />
          <v-select v-model="admissionForm.priority" :items="priorities" label="Priority" required />
          <v-text-field v-model="admissionForm.paymentMethod" label="Payment method" required />
        </div>
        <v-textarea v-model="admissionForm.chiefComplaint" label="Chief complaint" rows="2" required />
        <v-textarea v-model="admissionForm.notes" label="Notes" rows="2" />
        <div class="actions">
          <v-btn color="primary" prepend-icon="mdi-clipboard-plus" type="submit" :loading="savingAdmission">
            Admit patient
          </v-btn>
        </div>
      </v-form>
    </v-sheet>

    <VisitHistory :selected-patient="selectedPatient" :visits="selectedVisits" />
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

import VisitHistory from '../components/VisitHistory.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const {
  admissionForm,
  departments,
  loadPatients,
  patientOptions,
  priorities,
  savingAdmission,
  selectedPatient,
  selectedVisits,
  submitAdmission,
  visitTypes,
} = useAdmissionsStore()

onMounted(loadPatients)
</script>
