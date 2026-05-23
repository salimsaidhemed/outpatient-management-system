<template>
  <section class="stack">
    <v-sheet class="panel access-denied" border>
      <v-icon icon="mdi-lock-alert-outline" color="warning" />
      <h2>Access denied</h2>
      <p>Your account does not include the role required for this workspace area.</p>
      <v-btn color="primary" variant="tonal" prepend-icon="mdi-view-dashboard-outline" :to="{ name: 'dashboard' }">
        Return to dashboard
      </v-btn>
    </v-sheet>
  </section>
</template>
