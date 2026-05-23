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
            v-for="item in visibleNavItems"
            :key="item.name"
            :prepend-icon="item.icon"
            :title="item.title"
            :to="{ name: item.name }"
            rounded="lg"
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

          <router-view />
        </v-container>
      </v-main>

      <ReceiptDialog v-model="receiptDialog" :receipt-data="receiptData" />
    </template>
  </v-app>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import ReceiptDialog from './components/ReceiptDialog.vue'
import { navItems } from './router'
import { getUserProfile, initAuth, login, logout } from './services/auth'
import { useAdmissionsStore } from './stores/admissionsStore'

const drawer = ref(true)
const authLoading = ref(true)
const user = ref({ authenticated: false, roles: [] })
const route = useRoute()
const { error, loadAll, receiptData, receiptDialog } = useAdmissionsStore()

const currentTitle = computed(() => route.meta.title || 'Outpatient Admissions')
const todayLabel = computed(() => new Intl.DateTimeFormat(undefined, { dateStyle: 'medium' }).format(new Date()))
const visibleNavItems = computed(() =>
  navItems.filter((item) => item.roles.some((role) => user.value.roles.includes(role))),
)

onMounted(async () => {
  await initAuth()
  user.value = getUserProfile()
  authLoading.value = false
  if (user.value.authenticated) {
    await loadAll()
  }
})
</script>
