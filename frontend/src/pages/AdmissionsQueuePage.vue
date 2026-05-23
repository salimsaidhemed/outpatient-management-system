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
            <td>
              <v-select
                v-if="canManageStatus"
                :items="admissionStatuses"
                :loading="updatingAdmissionId === admission.id"
                :model-value="admission.status"
                density="compact"
                hide-details
                style="max-width: 190px"
                @update:model-value="updateAdmissionStatus(admission.id, $event)"
              />
              <StatusChip v-else :status="admission.status" />
            </td>
            <td class="text-right table-actions">
              <v-btn icon="mdi-receipt-text" size="small" variant="text" @click="openReceipt(admission.id)" />
              <v-btn
                v-if="canManageStatus && admission.status !== 'Discharged'"
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

const {
  admissionStatuses,
  admissions,
  loadAdmissions,
  markDischarged,
  openReceipt,
  updateAdmissionStatus,
  updatingAdmissionId,
} = useAdmissionsStore()
const canManageStatus = computed(() => getUserProfile().roles.includes('admissions_admin'))

onMounted(loadAdmissions)
</script>
