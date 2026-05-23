<template>
  <section class="stack">
    <v-sheet class="panel" border>
      <div class="panel-header">
        <h2>Administration</h2>
        <v-chip color="primary" variant="tonal" prepend-icon="mdi-shield-account">Admin only</v-chip>
      </div>
      <div class="admin-grid">
        <v-sheet class="admin-item" border>
          <v-icon icon="mdi-account-key-outline" color="primary" />
          <div>
            <strong>Role-based access</strong>
            <span>Admin-only actions include discharge controls and this administration area.</span>
          </div>
        </v-sheet>
        <v-sheet class="admin-item" border>
          <v-icon icon="mdi-routes" color="secondary" />
          <div>
            <strong>Route structure</strong>
            <span>Each workflow is now addressable by URL and protected by route metadata.</span>
          </div>
        </v-sheet>
      </div>
    </v-sheet>
  </section>
</template>
