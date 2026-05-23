<template>
  <section class="stack">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <h2>Admissions queue</h2>
        <v-btn icon="mdi-refresh" variant="text" @click="loadAdmissions" />
      </div>
      <v-table density="comfortable">
        <thead>
          <tr>
            <th>No.</th>
            <th>Patient</th>
            <th>Visit</th>
            <th>Provider</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="admission in admissions" :key="admission.id">
            <td>{{ admission.admissionNo }}</td>
            <td>{{ admission.patient.fullName }}</td>
            <td>{{ admission.department }} · {{ admission.visitType }}</td>
            <td>{{ admission.provider }}</td>
            <td><StatusChip :status="admission.status" /></td>
            <td class="text-right table-actions">
              <v-btn icon="mdi-receipt-text" size="small" variant="text" @click="openReceipt(admission.id)" />
              <v-btn
                v-if="canDischarge && admission.status !== 'Discharged'"
                icon="mdi-logout"
                size="small"
                variant="text"
                @click="markDischarged(admission.id)"
              />
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-sheet>
  </section>
</template>

<script setup>
import { computed, onMounted } from 'vue'

import StatusChip from '../components/StatusChip.vue'
import { getUserProfile } from '../services/auth'
import { useAdmissionsStore } from '../stores/admissionsStore'

const { admissions, loadAdmissions, markDischarged, openReceipt } = useAdmissionsStore()
const canDischarge = computed(() => getUserProfile().roles.includes('admissions_admin'))

onMounted(loadAdmissions)
</script>
