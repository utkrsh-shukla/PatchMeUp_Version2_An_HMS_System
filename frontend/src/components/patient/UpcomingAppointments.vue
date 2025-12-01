<template>
  <div class="card mb-4">
    <div class="card-header">
      <h5 class="mb-0"><i class="bi bi-calendar-check"></i> Your Upcoming Appointments</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Doctor</th>
              <th>Specialization</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td>{{ formatDate(apt.date) }}</td>
              <td>{{ formatTime(apt.time) }}</td>
              <td>{{ apt.doctor?.name || 'N/A' }}</td>
              <td>{{ apt.doctor?.specialization || 'N/A' }}</td>
              <td>
                <span :class="getStatusClass(apt.status)">
                  {{ getStatusText(apt.status) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <router-link to="/patient/appointments" class="btn btn-primary">
        View All Appointments
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UpcomingAppointments',
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
