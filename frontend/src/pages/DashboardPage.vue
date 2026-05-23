<template>
  <section class="stack">
    <div class="metric-grid">
      <v-sheet class="metric-panel" border>
        <v-icon icon="mdi-account-group" color="primary" />
        <div>
          <span>Total patients</span>
          <strong>{{ dashboard.totalPatients }}</strong>
        </div>
      </v-sheet>
      <v-sheet class="metric-panel" border>
        <v-icon icon="mdi-stethoscope" color="success" />
        <div>
          <span>Active admissions</span>
          <strong>{{ dashboard.activeAdmissions }}</strong>
        </div>
      </v-sheet>
      <v-sheet class="metric-panel" border>
        <v-icon icon="mdi-calendar-today" color="accent" />
        <div>
          <span>Visits today</span>
          <strong>{{ dashboard.visitsToday }}</strong>
        </div>
      </v-sheet>
    </div>

    <div class="content-grid">
      <v-sheet class="panel" border>
        <div class="panel-header">
          <h2>Recent admissions</h2>
          <v-btn icon="mdi-refresh" variant="text" @click="loadAll" />
        </div>
        <v-table density="comfortable">
          <thead>
            <tr>
              <th>Admission</th>
              <th>Patient</th>
              <th>Department</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="admission in dashboard.recentAdmissions" :key="admission.id">
              <td>{{ admission.admissionNo }}</td>
              <td>{{ admission.patient.fullName }}</td>
              <td>{{ admission.department }}</td>
              <td><StatusChip :status="admission.status" /></td>
            </tr>
          </tbody>
        </v-table>
      </v-sheet>

      <v-sheet class="panel" border>
        <div class="panel-header">
          <h2>Department load</h2>
        </div>
        <div class="load-list">
          <div v-for="item in dashboard.departmentLoad" :key="item.department" class="load-row">
            <span>{{ item.department }}</span>
            <v-progress-linear :model-value="loadPercent(item.count)" color="primary" height="8" rounded />
            <strong>{{ item.count }}</strong>
          </div>
          <v-empty-state
            v-if="!dashboard.departmentLoad.length"
            icon="mdi-chart-bar"
            text="Admissions by department will appear here."
            title="No visits yet"
          />
        </div>
      </v-sheet>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'

import StatusChip from '../components/StatusChip.vue'
import { useAdmissionsStore } from '../stores/admissionsStore'

const { dashboard, loadAll, loadPercent } = useAdmissionsStore()

onMounted(loadAll)
</script>
