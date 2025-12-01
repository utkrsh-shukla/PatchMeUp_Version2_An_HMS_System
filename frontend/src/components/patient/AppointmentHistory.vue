<template>
  <div class="card">
    <div class="card-header">
      <h5 class="mb-0">Past Appointments & Medical History</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Date</th>
              <th>Doctor</th>
              <th>Specialization</th>
              <th>Status</th>
              <th>Diagnosis</th>
              <th>Prescription</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="apt in appointments" :key="apt.id">
              <td><DateTimeDisplay :date="apt.date" format="date" /></td>
              <td>{{ apt.doctor_name }}</td>
              <td>{{ apt.doctor_specialization }}</td>
              <td><StatusBadge :status="apt.status" /></td>
              <td>
                <template v-if="apt.treatment">
                  {{ apt.treatment.diagnosis ? apt.treatment.diagnosis.substring(0, 50) + '...' : 'N/A' }}
                </template>
                <span v-else class="text-muted">N/A</span>
              </td>
              <td>
                <template v-if="apt.treatment && apt.treatment.prescription">
                  {{ apt.treatment.prescription.substring(0, 50) }}
                </template>
                <span v-else class="text-muted">N/A</span>
              </td>
            </tr>
            <tr v-if="!appointments || appointments.length === 0">
              <td colspan="6" class="text-center text-muted">No past appointments</td>
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
  name: 'AppointmentHistory',
  components: {
    DateTimeDisplay,
    StatusBadge
  },
  props: {
    appointments: {
      type: Array,
      default: () => []
    }
  }
}
</script>
