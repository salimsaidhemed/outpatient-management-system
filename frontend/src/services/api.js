import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5050/api',
})

export async function getDashboard() {
  const { data } = await api.get('/dashboard')
  return data
}

export async function getPatients(query = '') {
  const { data } = await api.get('/patients', { params: { q: query } })
  return data.patients
}

export async function createPatient(payload) {
  const { data } = await api.post('/patients', payload)
  return data
}

export async function getPatient(patientId) {
  const { data } = await api.get(`/patients/${patientId}`)
  return data
}

export async function getAdmissions() {
  const { data } = await api.get('/admissions')
  return data.admissions
}

export async function createAdmission(payload) {
  const { data } = await api.post('/admissions', payload)
  return data
}

export async function dischargeAdmission(admissionId) {
  const { data } = await api.patch(`/admissions/${admissionId}/discharge`)
  return data
}

export async function getReceipt(admissionId) {
  const { data } = await api.get(`/admissions/${admissionId}/receipt`)
  return data
}
