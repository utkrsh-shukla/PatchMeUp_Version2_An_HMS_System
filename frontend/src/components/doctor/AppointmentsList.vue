<template>
  <div class="card">
    <div class="card-header">
      <h5 class="mb-0">{{ title }}</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Patient</th>
              <th>Status</th>
              <th>Notes</th>
              <th v-if="showActions">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in appointments" :key="appointment.id">
              <td>{{ formatDate(appointment.date) }}</td>
              <td>{{ formatTime(appointment.time) }}</td>
              <td>
                <div>
                  <strong>{{ appointment.patient?.name || 'N/A' }}</strong>
                  <br>
                  <small class="text-muted">{{ appointment.patient?.phone || 'No phone' }}</small>
                </div>
              </td>
              <td>
                <span :class="getStatusClass(appointment.status)">
                  {{ getStatusText(appointment.status) }}
                </span>
              </td>
              <td>
                <span v-if="appointment.notes" class="text-truncate d-inline-block" style="max-width: 200px;">
                  {{ appointment.notes }}
                </span>
                <span v-else class="text-muted">No notes</span>
              </td>
              <td v-if="showActions">
                <div class="btn-group btn-group-sm">
                  <!-- View Patient History -->
                  <button 
                    @click="$emit('view-history', appointment.patient_id)"
                    class="btn btn-outline-info"
                    title="View Patient History"
                  >
                    <i class="bi bi-clock-history"></i>
                  </button>
                  
                  <!-- Add Treatment (only for booked appointments) -->
                  <button 
                    v-if="appointment.status === 'booked' && !appointment.treatment"
                    @click="$emit('add-treatment', appointment)"
                    class="btn btn-outline-success"
                    title="Add Treatment"
                  >
                    <i class="bi bi-plus-circle"></i>
                  </button>
                  
                  <!-- Complete Appointment -->
                  <button 
                    v-if="appointment.status === 'booked'"
                    @click="$emit('complete', appointment.id)"
                    class="btn btn-outline-primary"
                    title="Mark as Completed"
                  >
                    <i class="bi bi-check-circle"></i>
                  </button>
                  
                  <!-- Cancel Appointment -->
                  <button 
                    v-if="appointment.status === 'booked'"
                    @click="$emit('cancel', appointment.id)"
                    class="btn btn-outline-danger"
                    title="Cancel Appointment"
                  >
                    <i class="bi bi-x-circle"></i>
                  </button>
                  
                  <!-- Edit Treatment (if exists) -->
                  <button 
                    v-if="appointment.treatment"
                    class="btn btn-outline-warning"
                    title="Edit Treatment"
                    @click="$emit('edit-treatment', appointment)"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  
                  <!-- View Treatment (if exists) -->
                  <button 
                    v-if="appointment.treatment"
                    class="btn btn-outline-secondary"
                    title="View Treatment"
                    @click="showTreatment(appointment.treatment)"
                  >
                    <i class="bi bi-file-medical"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!appointments || appointments.length === 0">
              <td :colspan="showActions ? 6 : 5" class="text-center text-muted py-4">
                No appointments found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppointmentsList',
  props: {
    appointments: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: 'Appointments'
    },
    showActions: {
      type: Boolean,
      default: false
    }
  },
  emits: ['complete', 'cancel', 'add-treatment', 'edit-treatment', 'view-history'],
  methods: {
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    formatTime(timeStr) {
      return new Date(`2000-01-01T${timeStr}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    getStatusClass(status) {
      const classes = {
        'booked': 'badge bg-primary',
        'completed': 'badge bg-success',
        'cancelled': 'badge bg-danger',
        'rescheduled': 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    },
    
    getStatusText(status) {
      const texts = {
        'booked': 'Booked',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
        'rescheduled': 'Rescheduled'
      }
      return texts[status] || status
    },
    
    showTreatment(treatment) {
      alert(`Diagnosis: ${treatment.diagnosis}\n\nPrescription: ${treatment.prescription || 'None'}\n\nNotes: ${treatment.notes || 'None'}`)
    }
  }
}
</script>