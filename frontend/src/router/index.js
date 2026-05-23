import { createRouter, createWebHistory } from 'vue-router'

import AccessDeniedPage from '../pages/AccessDeniedPage.vue'
import AdminPage from '../pages/AdminPage.vue'
import AdmissionsQueuePage from '../pages/AdmissionsQueuePage.vue'
import AdmitOutpatientPage from '../pages/AdmitOutpatientPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import PatientDetailPage from '../pages/PatientDetailPage.vue'
import PatientSearchPage from '../pages/PatientSearchPage.vue'
import RegisterPatientPage from '../pages/RegisterPatientPage.vue'
import { getUserProfile, initAuth } from '../services/auth'

export const navItems = [
  {
    title: 'Dashboard',
    name: 'dashboard',
    path: '/',
    icon: 'mdi-view-dashboard-outline',
    component: DashboardPage,
    roles: ['admissions_user', 'admissions_admin'],
  },
  {
    title: 'Patients',
    name: 'patients',
    path: '/patients',
    icon: 'mdi-account-search-outline',
    component: PatientSearchPage,
    roles: ['admissions_user', 'admissions_admin'],
  },
  {
    title: 'Register patient',
    name: 'register',
    path: '/patients/register',
    icon: 'mdi-account-plus-outline',
    component: RegisterPatientPage,
    roles: ['admissions_user', 'admissions_admin'],
  },
  {
    title: 'Admit outpatient',
    name: 'admit',
    path: '/admissions/new',
    icon: 'mdi-clipboard-plus-outline',
    component: AdmitOutpatientPage,
    roles: ['admissions_user', 'admissions_admin'],
  },
  {
    title: 'Admissions',
    name: 'admissions',
    path: '/admissions',
    icon: 'mdi-format-list-checks',
    component: AdmissionsQueuePage,
    roles: ['admissions_user', 'admissions_admin'],
  },
  {
    title: 'Admin',
    name: 'admin',
    path: '/admin',
    icon: 'mdi-shield-account-outline',
    component: AdminPage,
    roles: ['admissions_admin'],
  },
]

const routes = [
  ...navItems.map(({ component, name, path, roles, title }) => ({
    component,
    name,
    path,
    meta: { requiresAuth: true, roles, title },
  })),
  {
    component: PatientDetailPage,
    name: 'patient-detail',
    path: '/patients/:patientId',
    meta: {
      requiresAuth: true,
      roles: ['admissions_user', 'admissions_admin'],
      title: 'Patient detail',
    },
  },
  {
    redirect: { name: 'patients' },
    path: '/patients/history',
  },
  {
    component: AccessDeniedPage,
    name: 'access-denied',
    path: '/access-denied',
    meta: { requiresAuth: true, title: 'Access denied' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  await initAuth()
  const user = getUserProfile()
  if (!to.meta.requiresAuth || !user.authenticated) return true

  const allowedRoles = to.meta.roles || []
  if (!allowedRoles.length) return true

  return allowedRoles.some((role) => user.roles.includes(role)) ? true : { name: 'access-denied' }
})

export default router
