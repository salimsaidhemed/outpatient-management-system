import axios from 'axios'

import { getToken } from './auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5050/api',
})

api.interceptors.request.use(async (config) => {
  const token = await getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
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

export async function updatePatient(patientId, payload) {
  const { data } = await api.patch(`/patients/${patientId}`, payload)
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

export async function updateAdmissionStatus(admissionId, status) {
  const { data } = await api.patch(`/admissions/${admissionId}/status`, { status })
  return data
}

export async function getReceipt(admissionId) {
  const { data } = await api.get(`/admissions/${admissionId}/receipt`)
  return data
}
