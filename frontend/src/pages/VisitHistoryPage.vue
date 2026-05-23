<template>
  <section class="stack">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <h2>Visit history</h2>
        <v-text-field
          v-model="patientSearch"
          density="compact"
          hide-details
          label="Search patients"
          prepend-inner-icon="mdi-magnify"
          style="max-width: 320px"
          @update:model-value="loadPatients"
        />
      </div>
      <v-table density="comfortable">
        <thead>
          <tr>
            <th>Patient</th>
            <th>MRN</th>
            <th>Age</th>
            <th>Phone</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.fullName }}</td>
            <td>{{ patient.mrn }}</td>
            <td>{{ patient.age }}</td>
            <td>{{ patient.phone }}</td>
            <td class="text-right">
              <v-btn icon="mdi-history" size="small" variant="text" @click="selectPatient(patient)" />
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-sheet>

    <VisitHistory :selected-patient="selectedPatient" :visits="selectedVisits" />
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

import VisitHistory from '../components/VisitHistory.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const { loadPatients, patientSearch, patients, selectPatient, selectedPatient, selectedVisits } =
  useAdmissionsStore()

onMounted(loadPatients)
</script>
