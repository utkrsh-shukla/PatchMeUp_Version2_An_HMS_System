<template>
  <div class="card mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0"><i class="bi bi-calendar-check"></i> Upcoming Appointments</h5>
      <router-link to="/admin/appointments" class="btn btn-sm btn-primary">View All</router-link>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Patient Name</th>
              <th>Doctor Name</th>
              <th>Department</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td>{{ apt.id }}</td>
              <td>{{ apt.patient?.name || 'N/A' }}</td>
              <td>{{ apt.doctor?.name || 'N/A' }}</td>
              <td>{{ apt.doctor?.department || 'N/A' }}</td>
              <td>{{ formatDate(apt.date) }}</td>
              <td>{{ formatTime(apt.time) }}</td>
              <td>
                <span :class="getStatusClass(apt.status)">
                  {{ getStatusText(apt.status) }}
                </span>
              </td>
            </tr>
            <tr v-if="!appointments || appointments.length === 0">
              <td colspan="7" class="text-center text-muted">No upcoming appointments</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppointmentsSection',
  props: {
    appointments: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    formatTime(timeStr) {
      if (!timeStr) return ''
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
    }
  }
}
</script>
