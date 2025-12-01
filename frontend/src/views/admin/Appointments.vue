<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-calendar-check"></i> Manage Appointments</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Filter Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'upcoming' }"
            @click="activeTab = 'upcoming'"
          >
            <i class="bi bi-calendar-plus"></i> Upcoming ({{ upcomingAppointments.length }})
          </button>
        </li>
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'all' }"
            @click="activeTab = 'all'"
          >
            <i class="bi bi-calendar3"></i> All Appointments ({{ allAppointments.length }})
          </button>
        </li>
      </ul>

      <!-- Upcoming Appointments -->
      <div v-if="activeTab === 'upcoming'">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Upcoming Appointments</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Patient</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Notes</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appointment in upcomingAppointments" :key="appointment.id">
                    <td>{{ appointment.id }}</td>
                    <td>{{ appointment.patient?.name || 'N/A' }}</td>
                    <td>{{ appointment.doctor?.name || 'N/A' }}</td>
                    <td>{{ appointment.doctor?.department || 'N/A' }}</td>
                    <td>{{ formatDate(appointment.date) }}</td>
                    <td>{{ formatTime(appointment.time) }}</td>
                    <td>
                      <span :class="getStatusClass(appointment.status)">
                        {{ getStatusText(appointment.status) }}
                      </span>
                    </td>
                    <td>
                      <span v-if="appointment.notes" class="text-truncate d-inline-block" style="max-width: 150px;">
                        {{ appointment.notes }}
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <router-link 
                          :to="`/admin/patients/${appointment.patient_id}/history`" 
                          class="btn btn-outline-info"
                          title="View Patient History"
                        >
                          <i class="bi bi-clock-history"></i>
                        </router-link>
                        <button 
                          v-if="appointment.status === 'booked'"
                          @click="cancelAppointment(appointment.id)"
                          class="btn btn-outline-danger"
                          title="Cancel Appointment"
                        >
                          <i class="bi bi-x-circle"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="upcomingAppointments.length === 0">
                    <td colspan="9" class="text-center text-muted py-4">
                      No upcoming appointments
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- All Appointments -->
      <div v-if="activeTab === 'all'">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">All Appointments</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Patient</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Status</th>
                    <th>Treatment</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="appointment in allAppointments" :key="appointment.id">
                    <td>{{ appointment.id }}</td>
                    <td>{{ appointment.patient?.name || 'N/A' }}</td>
                    <td>{{ appointment.doctor?.name || 'N/A' }}</td>
                    <td>{{ appointment.doctor?.department || 'N/A' }}</td>
                    <td>{{ formatDate(appointment.date) }}</td>
                    <td>{{ formatTime(appointment.time) }}</td>
                    <td>
                      <span :class="getStatusClass(appointment.status)">
                        {{ getStatusText(appointment.status) }}
                      </span>
                    </td>
                    <td>
                      <span v-if="appointment.treatment">
                        <i class="bi bi-check-circle text-success" title="Treatment completed"></i>
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <router-link 
                          :to="`/admin/patients/${appointment.patient_id}/history`" 
                          class="btn btn-outline-info"
                          title="View Patient History"
                        >
                          <i class="bi bi-clock-history"></i>
                        </router-link>
                        <button 
                          v-if="appointment.treatment"
                          @click="viewTreatment(appointment.treatment)"
                          class="btn btn-outline-success"
                          title="View Treatment"
                        >
                          <i class="bi bi-file-medical"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="allAppointments.length === 0">
                    <td colspan="9" class="text-center text-muted py-4">
                      No appointments found
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import adminAPI from '@/api/admin'

export default {
  name: 'AdminAppointments',
  components: {
    LoadingSpinner
  },
  setup() {
    const loading = ref(true)
    const activeTab = ref('upcoming')
    const upcomingAppointments = ref([])
    const allAppointments = ref([])

    const fetchAppointments = async () => {
      try {
        loading.value = true
        const [upcomingResponse, allResponse] = await Promise.all([
          adminAPI.getUpcomingAppointments(),
          adminAPI.getAppointments()
        ])
        
        upcomingAppointments.value = upcomingResponse.data.data
        allAppointments.value = allResponse.data.data
      } catch (error) {
        console.error('Error fetching appointments:', error)
        alert('Error loading appointments')
      } finally {
        loading.value = false
      }
    }

    const cancelAppointment = async (appointmentId) => {
      if (confirm('Are you sure you want to cancel this appointment?')) {
        try {
          // Note: We'll need to add this endpoint to the admin API
          // await adminAPI.cancelAppointment(appointmentId)
          alert('Cancel appointment functionality needs to be implemented in the backend')
          // await fetchAppointments()
        } catch (error) {
          console.error('Error cancelling appointment:', error)
          alert('Error cancelling appointment')
        }
      }
    }

    const viewTreatment = (treatment) => {
      alert(`Diagnosis: ${treatment.diagnosis}\n\nPrescription: ${treatment.prescription || 'None'}\n\nNotes: ${treatment.notes || 'None'}`)
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
      fetchAppointments()
    })

    return {
      loading,
      activeTab,
      upcomingAppointments,
      allAppointments,
      cancelAppointment,
      viewTreatment,
      formatDate,
      formatTime,
      getStatusClass,
      getStatusText
    }
  }
}
</script>