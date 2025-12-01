<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2><i class="bi bi-clock-history"></i> Patient Medical History</h2>
      <router-link to="/admin/patients" class="btn btn-secondary">
        <i class="bi bi-arrow-left"></i> Back to Patients
      </router-link>
    </div>

    <LoadingSpinner v-if="loading" />
    
    <template v-else-if="patientData">
      <!-- Patient Info Card -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0"><i class="bi bi-person"></i> Patient Information</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>Name:</strong> {{ patientData.name }}</p>
              <p><strong>Email:</strong> {{ patientData.email }}</p>
              <p><strong>Phone:</strong> {{ patientData.phone || 'N/A' }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Blood Group:</strong> {{ patientData.blood_group || 'N/A' }}</p>
              <p><strong>Date of Birth:</strong> {{ formatDate(patientData.date_of_birth) || 'N/A' }}</p>
              <p><strong>Address:</strong> {{ patientData.address || 'N/A' }}</p>
            </div>
          </div>
          <div v-if="patientData.medical_history">
            <p><strong>Medical History:</strong></p>
            <p class="text-muted">{{ patientData.medical_history }}</p>
          </div>
        </div>
      </div>

      <!-- Appointment History -->
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0"><i class="bi bi-calendar-check"></i> Appointment History</h5>
        </div>
        <div class="card-body">
          <div v-if="patientData.appointments && patientData.appointments.length > 0">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Doctor</th>
                    <th>Status</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appointment in patientData.appointments" :key="appointment.id">
                    <td>{{ formatDate(appointment.date) }}</td>
                    <td>{{ formatTime(appointment.time) }}</td>
                    <td>{{ appointment.doctor.name }}</td>
                    <td>
                      <span :class="getStatusClass(appointment.status)">
                        {{ getStatusText(appointment.status) }}
                      </span>
                    </td>
                    <td>
                      <span v-if="appointment.treatment">
                        {{ appointment.treatment.diagnosis }}
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                    <td>
                      <span v-if="appointment.treatment && appointment.treatment.prescription">
                        {{ appointment.treatment.prescription }}
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                    <td>
                      <span v-if="appointment.treatment && appointment.treatment.notes">
                        {{ appointment.treatment.notes }}
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else class="text-center text-muted py-4">
            <i class="bi bi-calendar-x fs-1"></i>
            <p class="mt-2">No appointment history found</p>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="text-center text-muted py-5">
      <i class="bi bi-exclamation-triangle fs-1"></i>
      <p class="mt-2">Patient not found</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import adminAPI from '@/api/admin'

export default {
  name: 'PatientHistory',
  components: {
    LoadingSpinner
  },
  setup() {
    const route = useRoute()
    const loading = ref(true)
    const patientData = ref(null)

    const fetchPatientHistory = async () => {
      try {
        loading.value = true
        const patientId = route.params.id
        const response = await adminAPI.getPatientHistory(patientId)
        patientData.value = response.data.data
      } catch (error) {
        console.error('Error fetching patient history:', error)
        alert('Error loading patient history')
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      return new Date(`2000-01-01T${timeStr}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getStatusClass = (status) => {
      const classes = {
        'booked': 'badge bg-primary',
        'completed': 'badge bg-success',
        'cancelled': 'badge bg-danger',
        'rescheduled': 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    }

    const getStatusText = (status) => {
      const texts = {
        'booked': 'Booked',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
        'rescheduled': 'Rescheduled'
      }
      return texts[status] || status
    }

    onMounted(() => {
      fetchPatientHistory()
    })

    return {
      loading,
      patientData,
      formatDate,
      formatTime,
      getStatusClass,
      getStatusText
    }
  }
}
</script>