<template>
  <div class="card">
    <div class="card-header">
      <h5 class="mb-0"><i class="bi bi-calendar-week"></i> Upcoming Appointments (Next 7 Days)</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Patient</th>
              <th>Phone</th>
              <th>Notes</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td><DateTimeDisplay :date="apt.date" format="date" /></td>
              <td><DateTimeDisplay :time="apt.time" format="time" /></td>
              <td>{{ apt.patient?.name || 'N/A' }}</td>
              <td>{{ apt.patient?.phone || 'N/A' }}</td>
              <td>{{ truncate(apt.notes, 30) }}</td>
              <td><StatusBadge :status="apt.status" /></td>
              <td>
                <slot name="actions" :appointment="apt">
                  <div class="btn-group btn-group-sm">
                    <!-- Add Treatment (if no treatment exists) -->
                    <button 
                      v-if="!apt.treatment && apt.status === 'booked'"
                      @click="$emit('add-treatment', apt)"
                      class="btn btn-outline-success"
                      title="Add Treatment"
                    >
                      <i class="bi bi-plus-circle"></i>
                    </button>
                    
                    <!-- Edit Treatment (if treatment exists) -->
                    <button 
                      v-if="apt.treatment"
                      @click="$emit('edit-treatment', apt)"
                      class="btn btn-outline-warning"
                      title="Edit Treatment"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </button>
                    
                    <!-- View Patient History -->
                    <button 
                      @click="$emit('view-history', apt.patient_id)"
                      class="btn btn-outline-info"
                      title="View Patient History"
                    >
                      <i class="bi bi-clock-history"></i>
                    </button>
                  </div>
                </slot>
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
import DateTimeDisplay from '@/components/shared/DateTimeDisplay.vue'
import StatusBadge from '@/components/shared/StatusBadge.vue'

export default {
  name: 'DoctorUpcomingAppointments',
  components: {
    DateTimeDisplay,
    StatusBadge
  },
  props: {
    appointments: {
      type: Array,
      default: () => []
    }
  },
  emits: ['add-treatment', 'edit-treatment', 'view-history'],
  setup() {
    const truncate = (text, length) => {
      if (!text) return '-'
      return text.length > length ? text.substring(0, length) + '...' : text
    }
    
    return {
      truncate
    }
  }
}
</script>
