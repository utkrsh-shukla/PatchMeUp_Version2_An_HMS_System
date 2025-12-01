<template>
  <div class="card mb-4">
    <div class="card-header">
      <h5 class="mb-0"><i class="bi bi-calendar-day"></i> Today's Appointments</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Time</th>
              <th>Patient</th>
              <th>Phone</th>
              <th>Notes</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td><DateTimeDisplay :time="apt.time" format="time" /></td>
              <td>{{ apt.patient_name || apt.patient?.name }}</td>
              <td>{{ apt.patient_phone || apt.patient?.phone || 'N/A' }}</td>
              <td>{{ truncate(apt.notes, 50) }}</td>
              <td><StatusBadge :status="apt.status" /></td>
            </tr>
            <tr v-if="!appointments || appointments.length === 0">
              <td colspan="5" class="text-center text-muted">No appointments for today</td>
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
  name: 'TodaySchedule',
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
