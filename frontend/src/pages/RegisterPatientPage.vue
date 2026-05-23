<template>
  <section class="form-grid">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <h2>Register patient</h2>
      </div>
      <v-form @submit.prevent="submitPatient(() => router.push({ name: 'admit' }))">
        <div class="two-column">
          <v-text-field v-model="patientForm.firstName" label="First name" required />
          <v-text-field v-model="patientForm.lastName" label="Last name" required />
          <v-text-field v-model="patientForm.dateOfBirth" label="Date of birth" type="date" required />
          <v-select v-model="patientForm.sex" :items="sexOptions" label="Sex" required />
          <v-text-field v-model="patientForm.phone" label="Phone" required />
          <v-text-field v-model="patientForm.email" label="Email" type="email" />
        </div>
        <v-textarea v-model="patientForm.address" label="Address" rows="2" required />
        <v-text-field v-model="patientForm.emergencyContact" label="Emergency contact" />
        <div class="actions">
          <v-btn color="primary" prepend-icon="mdi-account-plus" type="submit" :loading="savingPatient">
            Save patient
          </v-btn>
        </div>
      </v-form>
    </v-sheet>

    <PatientList :patients="patients" @select="selectPatient" />
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

import PatientList from '../components/PatientList.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const router = useRouter()
const {
  loadPatients,
  patientForm,
  patients,
  savingPatient,
  selectPatient,
  sexOptions,
  submitPatient,
} = useAdmissionsStore()

onMounted(loadPatients)
</script>
