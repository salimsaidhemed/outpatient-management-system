<template>
  <v-dialog :model-value="modelValue" max-width="760" @update:model-value="$emit('update:modelValue', $event)">
    <v-sheet v-if="receiptData" class="receipt-shell">
      <div class="receipt-actions no-print">
        <v-btn icon="mdi-printer" color="primary" @click="printReceipt" />
        <v-btn icon="mdi-close" variant="text" @click="$emit('update:modelValue', false)" />
      </div>

      <div id="printable-receipt" class="receipt">
        <header class="receipt-header">
          <div>
            <h1>{{ receiptData.facility.name }}</h1>
            <p>{{ receiptData.facility.address }} · {{ receiptData.facility.phone }}</p>
          </div>
          <div class="receipt-no">
            <span>Admission receipt</span>
            <strong>{{ receiptData.receipt.admissionNo }}</strong>
          </div>
        </header>

        <div class="receipt-section">
          <h2>Patient</h2>
          <div class="receipt-grid">
            <span>Name</span><strong>{{ receiptData.receipt.patient.fullName }}</strong>
            <span>MRN</span><strong>{{ receiptData.receipt.patient.mrn }}</strong>
            <span>DOB / Age</span><strong>{{ receiptData.receipt.patient.dateOfBirth }} / {{ receiptData.receipt.patient.age }}</strong>
            <span>Phone</span><strong>{{ receiptData.receipt.patient.phone }}</strong>
          </div>
        </div>

        <div class="receipt-section">
          <h2>Visit</h2>
          <div class="receipt-grid">
            <span>Department</span><strong>{{ receiptData.receipt.department }}</strong>
            <span>Provider</span><strong>{{ receiptData.receipt.provider }}</strong>
            <span>Visit type</span><strong>{{ receiptData.receipt.visitType }}</strong>
            <span>Priority</span><strong>{{ receiptData.receipt.priority }}</strong>
            <span>Payment</span><strong>{{ receiptData.receipt.paymentMethod }}</strong>
            <span>Admitted</span><strong>{{ formatDate(receiptData.receipt.admittedAt) }}</strong>
          </div>
        </div>

        <div class="receipt-section">
          <h2>Chief complaint</h2>
          <p>{{ receiptData.receipt.chiefComplaint }}</p>
        </div>

        <footer class="receipt-footer">
          <span>Issued {{ formatDate(receiptData.issuedAt) }}</span>
          <span>Front desk signature ____________________</span>
        </footer>
      </div>
    </v-sheet>
  </v-dialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  receiptData: {
    type: Object,
    default: null,
  },
})

defineEmits(['update:modelValue'])

function printReceipt() {
  window.print()
}

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value))
}
</script>
