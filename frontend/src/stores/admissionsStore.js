import { computed, reactive, ref } from 'vue'

import {
  createAdmission,
  createPatient,
  dischargeAdmission,
  getAdmissions,
  getDashboard,
  getPatient,
  getPatients,
  getReceipt,
  updateAdmissionStatus as patchAdmissionStatus,
  updatePatient,
} from '../services/api'

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
const editingPatient = ref(false)
const savingPatientEdit = ref(false)
const updatingAdmissionId = ref(null)

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

const patientEditForm = reactive({
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

const sexOptions = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
const departments = ['General Medicine', 'Cardiology', 'Orthopedics', 'Pediatrics', 'Dermatology', 'Diagnostics']
const visitTypes = ['Consultation', 'Follow-up', 'Procedure', 'Lab review', 'Urgent outpatient']
const priorities = ['Routine', 'Priority', 'Urgent']
const admissionStatuses = ['Admitted', 'In Progress', 'Ready for Discharge', 'Discharged', 'Cancelled']

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

function preparePatientEdit(patient = selectedPatient.value) {
  if (!patient) return
  Object.assign(patientEditForm, {
    firstName: patient.firstName,
    lastName: patient.lastName,
    dateOfBirth: patient.dateOfBirth,
    sex: patient.sex,
    phone: patient.phone,
    email: patient.email || '',
    address: patient.address,
    emergencyContact: patient.emergencyContact || '',
  })
  editingPatient.value = true
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

async function submitPatient(afterCreate) {
  savingPatient.value = true
  const patient = await withErrorHandling(() => createPatient({ ...patientForm }))
  savingPatient.value = false
  if (!patient) return
  resetPatientForm()
  await loadPatients()
  await selectPatient(patient)
  if (afterCreate) afterCreate(patient)
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
  return data
}

async function loadPatientDetail(patientId) {
  const data = await withErrorHandling(() => getPatient(patientId))
  if (!data) return
  selectedPatient.value = data.patient
  selectedVisits.value = data.visits
  admissionForm.patientId = data.patient.id
  return data
}

async function savePatientEdit() {
  if (!selectedPatient.value) return null
  savingPatientEdit.value = true
  const patient = await withErrorHandling(() => updatePatient(selectedPatient.value.id, { ...patientEditForm }))
  savingPatientEdit.value = false
  if (!patient) return null
  selectedPatient.value = patient
  editingPatient.value = false
  await loadPatients()
  return patient
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

async function updateAdmissionStatus(admissionId, status) {
  updatingAdmissionId.value = admissionId
  const admission = await withErrorHandling(() => patchAdmissionStatus(admissionId, status))
  updatingAdmissionId.value = null
  if (!admission) return null

  admissions.value = admissions.value.map((item) => (item.id === admission.id ? admission : item))
  dashboard.recentAdmissions = dashboard.recentAdmissions.map((item) =>
    item.id === admission.id ? admission : item,
  )
  selectedVisits.value = selectedVisits.value.map((visit) => (visit.id === admission.id ? admission : visit))
  await loadDashboard()
  return admission
}

function loadPercent(count) {
  const max = Math.max(...dashboard.departmentLoad.map((item) => item.count), 1)
  return Math.round((count / max) * 100)
}

export function useAdmissionsStore() {
  return {
    admissionForm,
    admissionStatuses,
    admissions,
    dashboard,
    departments,
    editingPatient,
    error,
    loadAdmissions,
    loadAll,
    loadDashboard,
    loadPatients,
    loadPatientDetail,
    loadPercent,
    markDischarged,
    openReceipt,
    patientEditForm,
    patientForm,
    patientOptions,
    patientSearch,
    patients,
    preparePatientEdit,
    priorities,
    receiptData,
    receiptDialog,
    savingAdmission,
    savingPatient,
    savePatientEdit,
    savingPatientEdit,
    selectPatient,
    selectedPatient,
    selectedVisits,
    sexOptions,
    submitAdmission,
    submitPatient,
    updateAdmissionStatus,
    updatingAdmissionId,
    visitTypes,
  }
}
