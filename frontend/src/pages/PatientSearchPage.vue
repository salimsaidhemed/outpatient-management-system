<template>
  <section class="stack">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <div>
          <h2>Patient search</h2>
          <p class="panel-subtitle">Find a patient record, then open their demographic profile and visit history.</p>
        </div>
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
              <v-btn
                icon="mdi-card-account-details-outline"
                size="small"
                variant="text"
                :to="{ name: 'patient-detail', params: { patientId: patient.id } }"
              />
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-sheet>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

import { useAdmissionsStore } from '../stores/admissionsStore'

const { loadPatients, patientSearch, patients } = useAdmissionsStore()

onMounted(loadPatients)
</script>
