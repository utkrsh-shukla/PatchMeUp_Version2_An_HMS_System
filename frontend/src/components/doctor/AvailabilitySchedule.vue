<template>
  <div>
    <div v-for="day in 7" :key="day" class="mb-4">
      <h5 class="text-danger">{{ getDayName(day - 1) }}</h5>
      
      <div v-if="getDaySlots(day - 1).length > 0" class="table-responsive">
        <table class="table table-sm">
          <thead>
            <tr>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="slot in getDaySlots(day - 1)" :key="slot.id">
              <td>{{ formatTime(slot.start_time) }}</td>
              <td>{{ formatTime(slot.end_time) }}</td>
              <td>
                <span :class="slot.is_available ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ slot.is_available ? 'Available' : 'Unavailable' }}
                </span>
              </td>
              <td>
                <button @click="$emit('delete', slot.id)" class="btn btn-sm btn-danger">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <p v-else class="text-muted">No availability set for this day</p>
      
      <hr v-if="day < 7">
    </div>
  </div>
</template>

<script>
export default {
  name: 'AvailabilitySchedule',
  props: {
    weeklySchedule: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['delete'],
  data() {
    return {
      dayNames: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },
  methods: {
    getDayName(dayIndex) {
      return this.dayNames[dayIndex]
    },
    getDaySlots(dayIndex) {
      return this.weeklySchedule[dayIndex] || []
    },
    formatTime(timeStr) {
      if (!timeStr) return 'N/A'
      const date = new Date(`2000-01-01T${timeStr}`)
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>
