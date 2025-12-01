<template>
  <div class="card">
    <div v-if="title" class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">
        <i v-if="icon" :class="icon"></i> {{ title }}
      </h5>
      <slot name="header-actions"></slot>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="appointment in appointments" :key="appointment.id">
              <slot name="row" :appointment="appointment">
                <!-- Default row rendering -->
                <td v-for="column in columns" :key="column.key">
                  <template v-if="column.key === 'date'">
                    <DateTimeDisplay :date="appointment.date" format="date" />
                  </template>
                  <template v-else-if="column.key === 'time'">
                    <DateTimeDisplay :time="appointment.time" format="time" />
                  </template>
                  <template v-else-if="column.key === 'status'">
                    <StatusBadge :status="appointment.status" />
                  </template>
                  <template v-else>
                    {{ getColumnValue(appointment, column.key) }}
                  </template>
                </td>
              </slot>
            </tr>
            <tr v-if="!appointments || appointments.length === 0">
              <td :colspan="columns.length" class="text-center text-muted">
                {{ emptyMessage }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
import DateTimeDisplay from './DateTimeDisplay.vue'
import StatusBadge from './StatusBadge.vue'

export default {
  name: 'AppointmentTable',
  components: {
    DateTimeDisplay,
    StatusBadge
  },
  props: {
    appointments: {
      type: Array,
      default: () => []
    },
    columns: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: null
    },
    icon: {
      type: String,
      default: null
    },
    emptyMessage: {
      type: String,
      default: 'No appointments found'
    }
  },
  setup() {
    const getColumnValue = (appointment, key) => {
      // Handle nested keys like 'doctor_name', 'patient_name', etc.
      return appointment[key] || 'N/A'
    }
    
    return {
      getColumnValue
    }
  }
}
</script>
