<template>
  <v-app>
    <div v-if="authLoading" class="auth-screen">
      <v-progress-circular color="primary" indeterminate size="46" />
    </div>

    <div v-else-if="!user.authenticated" class="auth-screen">
      <div class="login-layout">
        <section class="login-copy">
          <div class="brand-block login-brand">
            <div class="brand-mark">OA</div>
            <div>
              <div class="brand-title">Outpatient Admissions</div>
              <div class="brand-subtitle">Front desk console</div>
            </div>
          </div>
          <h1>Secure admissions workspace</h1>
          <p>Register patients, manage outpatient visits, and print admission receipts from one controlled access console.</p>
          <div class="login-signals" aria-label="System highlights">
            <span><v-icon icon="mdi-shield-check" /> Keycloak protected</span>
            <span><v-icon icon="mdi-database-check" /> PostgreSQL backed</span>
            <span><v-icon icon="mdi-printer-check" /> Receipt ready</span>
          </div>
        </section>

        <v-sheet class="login-panel" border>
          <div class="login-panel-header">
            <v-icon icon="mdi-lock-outline" color="primary" />
            <span>Authorized staff only</span>
          </div>
          <h2>Sign in to continue</h2>
          <p>Use your admissions account to open the console.</p>
          <v-btn block color="primary" size="large" prepend-icon="mdi-login" @click="login">
            Sign in with Keycloak
          </v-btn>
        </v-sheet>
      </div>
    </div>

    <template v-else>
    <v-navigation-drawer v-model="drawer" class="app-sidebar" width="280">
      <div class="brand-block">
        <div class="brand-mark">OA</div>
        <div>
          <div class="brand-title">Outpatient Admissions</div>
          <div class="brand-subtitle">Front desk console</div>
        </div>
      </div>

      <v-list nav density="comfortable">
        <v-list-item
          v-for="item in navItems"
          :key="item.value"
          :active="activeTab === item.value"
          :prepend-icon="item.icon"
          :title="item.title"
          rounded="lg"
          @click="activeTab = item.value"
        />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar flat border color="surface">
      <v-app-bar-nav-icon class="d-md-none" @click="drawer = !drawer" />
      <v-toolbar-title>{{ currentTitle }}</v-toolbar-title>
      <v-spacer />
      <div class="appbar-actions">
        <v-chip color="secondary" variant="tonal" prepend-icon="mdi-account-circle">
          {{ user.name || user.username }}
        </v-chip>
        <v-chip color="primary" variant="tonal" prepend-icon="mdi-calendar-clock">
          {{ todayLabel }}
        </v-chip>
        <v-btn icon="mdi-logout" variant="text" @click="logout" />
      </div>
    </v-app-bar>

    <v-main>
      <v-container fluid class="page-shell">
        <v-alert
          v-if="error"
          class="mb-4"
          type="error"
          variant="tonal"
          closable
          @click:close="error = ''"
        >
          {{ error }}
        </v-alert>

        <section v-show="activeTab === 'dashboard'" class="stack">
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
                  <v-progress-linear
                    :model-value="loadPercent(item.count)"
                    color="primary"
                    height="8"
                    rounded
                  />
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

        <section v-show="activeTab === 'register'" class="form-grid">
          <v-sheet class="panel" border>
            <div class="panel-header">
              <h2>Register patient</h2>
            </div>
            <v-form @submit.prevent="submitPatient">
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

        <section v-show="activeTab === 'admit'" class="form-grid">
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

        <section v-show="activeTab === 'history'" class="stack">
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
                    <v-btn
                      icon="mdi-history"
                      size="small"
                      variant="text"
                      @click="selectPatient(patient)"
                    />
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-sheet>

          <VisitHistory :selected-patient="selectedPatient" :visits="selectedVisits" />
        </section>

        <section v-show="activeTab === 'admissions'" class="stack">
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
                    <v-btn
                      icon="mdi-receipt-text"
                      size="small"
                      variant="text"
                      @click="openReceipt(admission.id)"
                    />
                    <v-btn
                      v-if="admission.status !== 'Discharged'"
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
      </v-container>
    </v-main>

    <ReceiptDialog v-model="receiptDialog" :receipt-data="receiptData" />
    </template>
  </v-app>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import PatientList from './components/PatientList.vue'
import ReceiptDialog from './components/ReceiptDialog.vue'
import StatusChip from './components/StatusChip.vue'
import VisitHistory from './components/VisitHistory.vue'
import { getUserProfile, initAuth, login, logout } from './services/auth'
import {
  createAdmission,
  createPatient,
  dischargeAdmission,
  getAdmissions,
  getDashboard,
  getPatient,
  getPatients,
  getReceipt,
} from './services/api'

const drawer = ref(true)
const activeTab = ref('dashboard')
const authLoading = ref(true)
const user = ref({ authenticated: false })
const error = ref('')
const savingPatient = ref(false)
const savingAdmission = ref(false)
const receiptDialog = ref(false)
const receiptData = ref(null)
const patients = ref([])
const admissions = ref([])
const selectedPatient = ref(null)
const selectedVisits = ref([])
const patientSearch = ref('')

const dashboard = reactive({
  totalPatients: 0,
  activeAdmissions: 0,
  visitsToday: 0,
  recentAdmissions: [],
  departmentLoad: [],
})

const patientForm = reactive({
  firstName: '',
  lastName: '',
  dateOfBirth: '',
  sex: '',
  phone: '',
  email: '',
  address: '',
  emergencyContact: '',
})

const admissionForm = reactive({
  patientId: null,
  department: '',
  provider: '',
  visitType: '',
  chiefComplaint: '',
  priority: 'Routine',
  paymentMethod: 'Insurance',
  notes: '',
})

const navItems = [
  { title: 'Dashboard', value: 'dashboard', icon: 'mdi-view-dashboard-outline' },
  { title: 'Register patient', value: 'register', icon: 'mdi-account-plus-outline' },
  { title: 'Admit outpatient', value: 'admit', icon: 'mdi-clipboard-plus-outline' },
  { title: 'Admissions', value: 'admissions', icon: 'mdi-format-list-checks' },
  { title: 'Visit history', value: 'history', icon: 'mdi-history' },
]
const sexOptions = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
const departments = ['General Medicine', 'Cardiology', 'Orthopedics', 'Pediatrics', 'Dermatology', 'Diagnostics']
const visitTypes = ['Consultation', 'Follow-up', 'Procedure', 'Lab review', 'Urgent outpatient']
const priorities = ['Routine', 'Priority', 'Urgent']

const currentTitle = computed(() => navItems.find((item) => item.value === activeTab.value)?.title)
const todayLabel = computed(() => new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date()))
const patientOptions = computed(() =>
  patients.value.map((patient) => ({
    id: patient.id,
    label: `${patient.fullName} · ${patient.mrn}`,
  })),
)

function resetPatientForm() {
  Object.assign(patientForm, {
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    sex: '',
    phone: '',
    email: '',
    address: '',
    emergencyContact: '',
  })
}

function resetAdmissionForm(patientId = null) {
  Object.assign(admissionForm, {
    patientId,
    department: '',
    provider: '',
    visitType: '',
    chiefComplaint: '',
    priority: 'Routine',
    paymentMethod: 'Insurance',
    notes: '',
  })
}

async function withErrorHandling(action) {
  try {
    error.value = ''
    return await action()
  } catch (err) {
    error.value = err.response?.data?.error || err.message || 'Something went wrong'
    return null
  }
}

async function loadDashboard() {
  const data = await withErrorHandling(getDashboard)
  if (data) Object.assign(dashboard, data)
}

async function loadPatients() {
  patients.value = (await withErrorHandling(() => getPatients(patientSearch.value))) || []
}

async function loadAdmissions() {
  admissions.value = (await withErrorHandling(getAdmissions)) || []
}

async function loadAll() {
  await Promise.all([loadDashboard(), loadPatients(), loadAdmissions()])
}

async function submitPatient() {
  savingPatient.value = true
  const patient = await withErrorHandling(() => createPatient({ ...patientForm }))
  savingPatient.value = false
  if (!patient) return
  resetPatientForm()
  await loadPatients()
  await selectPatient(patient)
  activeTab.value = 'admit'
}

async function submitAdmission() {
  savingAdmission.value = true
  const admission = await withErrorHandling(() => createAdmission({ ...admissionForm }))
  savingAdmission.value = false
  if (!admission) return
  resetAdmissionForm(admission.patientId)
  await loadAll()
  await selectPatient(admission.patient)
  await openReceipt(admission.id)
}

async function selectPatient(patient) {
  const data = await withErrorHandling(() => getPatient(patient.id))
  if (!data) return
  selectedPatient.value = data.patient
  selectedVisits.value = data.visits
  admissionForm.patientId = data.patient.id
}

async function openReceipt(admissionId) {
  const data = await withErrorHandling(() => getReceipt(admissionId))
  if (!data) return
  receiptData.value = data
  receiptDialog.value = true
}

async function markDischarged(admissionId) {
  await withErrorHandling(() => dischargeAdmission(admissionId))
  await loadAll()
}

function loadPercent(count) {
  const max = Math.max(...dashboard.departmentLoad.map((item) => item.count), 1)
  return Math.round((count / max) * 100)
}

onMounted(async () => {
  await initAuth()
  user.value = getUserProfile()
  authLoading.value = false
  if (user.value.authenticated) {
    await loadAll()
  }
})
</script>
