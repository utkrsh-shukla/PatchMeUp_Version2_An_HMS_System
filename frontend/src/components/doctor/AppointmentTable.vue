<template>
  <DataTable
    :columns="columns"
    :data="appointments"
    empty-message="No appointments found"
  >
    <template #body="{ data }">
      <tr v-for="appointment in data" :key="appointment.id">
        <td>{{ formatDate(appointment.date) }}</td>
        <td>{{ formatTime(appointment.time) }}</td>
        <td>{{ appointment.patient_name }}</td>
        <td>{{ appointment.patient_phone || 'N/A' }}</td>
        <td>{{ truncate(appointment.notes, 40) }}</td>
        <td>
          <span :class="getBadgeClass(appointment.status)" class="badge">
            {{ appointment.status }}
          </span>
        </td>
        <td>
          <template v-if="['booked', 'rescheduled'].includes(appointment.status)">
            <button @click="$emit('add-treatment', appointment.id)" class="btn btn-sm btn-primary me-1" title="Add Treatment">
              <i class="bi bi-file-medical"></i>
            </button>
            <button @click="$emit('complete', appointment.id)" class="btn btn-sm btn-success me-1" title="Mark Complete">
              <i class="bi bi-check-circle"></i>
            </button>
            <button @click="$emit('cancel', appointment.id)" class="btn btn-sm btn-danger me-1" title="Cancel">
              <i class="bi bi-x-circle"></i>
            </button>
          </template>
          <button @click="$emit('view-history', appointment.patient_id)" class="btn btn-sm btn-secondary" title="View History">
            <i class="bi bi-clock-history"></i>
          </button>
        </td>
      </tr>
    </template>
  </DataTable>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'

export default {
  name: 'AppointmentTable',
  components: {
    DataTable
  },
  props: {
    appointments: {
      type: Array,
      default: () => []
    }
  },
  emits: ['add-treatment', 'complete', 'cancel', 'view-history'],
  data() {
    return {
      columns: [
        { key: 'date', label: 'Date' },
        { key: 'time', label: 'Time' },
        { key: 'patient', label: 'Patient' },
        { key: 'phone', label: 'Phone' },
        { key: 'notes', label: 'Notes' },
        { key: 'status', label: 'Status' },
        { key: 'actions', label: 'Actions' }
      ]
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return 'N/A'
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    },
    formatTime(timeStr) {
      if (!timeStr) return 'N/A'
      const date = new Date(`2000-01-01T${timeStr}`)
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    },
    truncate(text, length) {
      if (!text) return '-'
      return text.length > length ? text.substring(0, length) + '...' : text
    },
    getBadgeClass(status) {
      return `badge-${status}`
    }
  }
}
</script>
