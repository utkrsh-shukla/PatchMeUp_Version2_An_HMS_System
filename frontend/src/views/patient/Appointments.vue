<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-calendar-check"></i> My Appointments</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Upcoming Appointments -->
      <div class="mb-5">
        <h4 class="mb-3 text-muted">Upcoming Appointments</h4>
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead class="table-light">
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="appointment in upcomingAppointments" :key="appointment.id">
                <td>{{ formatDate(appointment.date) }}</td>
                <td>{{ formatTime(appointment.time) }}</td>
                <td>{{ appointment.doctor?.name || 'N/A' }}</td>
                <td>{{ appointment.doctor?.specialization || 'N/A' }}</td>
                <td>
                  <span :class="getStatusClass(appointment.status)">
                    {{ getStatusText(appointment.status) }}
                  </span>
                </td>
                <td>
                  <div v-if="appointment.status === 'booked' || appointment.status === 'rescheduled'" class="d-flex gap-1">
                    <button 
                      @click="rescheduleAppointment(appointment)"
                      class="btn btn-sm btn-outline-warning"
                      title="Reschedule Appointment"
                    >
                      Reschedule
                    </button>
                    <button 
                      @click="cancelAppointment(appointment.id)"
                      class="btn btn-sm btn-outline-danger"
                      title="Cancel Appointment"
                    >
                      Cancel
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="upcomingAppointments.length === 0">
                <td colspan="6" class="text-center text-muted py-3">
                  No upcoming appointments
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Past Appointments & Medical History -->
      <div>
        <h4 class="mb-3 text-muted">Past Appointments & Medical History</h4>
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead class="table-light">
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
              <tr v-for="appointment in pastAppointments" :key="appointment.id">
                <td>{{ formatDate(appointment.date) }}</td>
                <td>{{ appointment.doctor?.name || 'N/A' }}</td>
                <td>{{ appointment.doctor?.specialization || 'N/A' }}</td>
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
              </tr>
              <tr v-if="pastAppointments.length === 0">
                <td colspan="6" class="text-center text-muted py-3">
                  No past appointments
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- Reschedule Appointment Modal -->
    <div v-if="showRescheduleModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reschedule Appointment</h5>
            <button type="button" class="btn-close" @click="closeRescheduleModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="appointmentToReschedule">
              <p><strong>Doctor:</strong> {{ appointmentToReschedule.doctor?.name }}</p>
              <p><strong>Current Date:</strong> {{ formatDate(appointmentToReschedule.date) }}</p>
              <p><strong>Current Time:</strong> {{ formatTime(appointmentToReschedule.time) }}</p>
              
              <form @submit.prevent="submitReschedule">
                <div class="mb-3">
                  <label for="rescheduleDate" class="form-label">New Date</label>
                  <input 
                    id="rescheduleDate" 
                    v-model="rescheduleForm.date" 
                    type="date" 
                    class="form-control" 
                    :min="minDate"
                    required 
                  />
                </div>
                
                <div class="mb-3">
                  <label for="rescheduleTime" class="form-label">New Time</label>
                  <select id="rescheduleTime" v-model="rescheduleForm.time" class="form-select" required>
                    <option value="">Select Time</option>
                    <option 
                      v-for="time in availableTimes" 
                      :key="time" 
                      :value="time"
                      :disabled="bookedTimes.includes(time)"
                    >
                      {{ formatTime(time) }} {{ bookedTimes.includes(time) ? '(Booked)' : '' }}
                    </option>
                  </select>
                </div>

                <div class="d-flex justify-content-end gap-2">
                  <button type="button" @click="closeRescheduleModal" class="btn btn-secondary">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-warning">
                    Reschedule
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import patientAPI from '@/api/patient'

export default {
  name: 'PatientAppointments',
  components: {
    LoadingSpinner
  },
  setup() {
    const loading = ref(true)
    const upcomingAppointments = ref([])
    const pastAppointments = ref([])
    const showRescheduleModal = ref(false)
    const appointmentToReschedule = ref(null)
    const rescheduleForm = ref({
      date: '',
      time: ''
    })
    const bookedTimes = ref([])

    const fetchAppointments = async () => {
      try {
        loading.value = true
        const [upcomingResponse, pastResponse] = await Promise.all([
          patientAPI.getUpcomingAppointments(),
          patientAPI.getPastAppointments()
        ])
        
        upcomingAppointments.value = upcomingResponse.data.data
        pastAppointments.value = pastResponse.data.data
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
          await patientAPI.cancelAppointment(appointmentId)
          await fetchAppointments()
          alert('Appointment cancelled successfully')
        } catch (error) {
          console.error('Error cancelling appointment:', error)
          alert('Error cancelling appointment')
        }
      }
    }

    const rescheduleAppointment = (appointment) => {
      appointmentToReschedule.value = appointment
      rescheduleForm.value = {
        date: '',
        time: ''
      }
      showRescheduleModal.value = true
    }

    const submitReschedule = async () => {
      try {
        await patientAPI.rescheduleAppointment(appointmentToReschedule.value.id, rescheduleForm.value)
        closeRescheduleModal()
        await fetchAppointments()
        alert('Appointment rescheduled successfully!')
      } catch (error) {
        console.error('Error rescheduling appointment:', error)
        alert(error.response?.data?.error || 'Error rescheduling appointment')
      }
    }

    const closeRescheduleModal = () => {
      showRescheduleModal.value = false
      appointmentToReschedule.value = null
      rescheduleForm.value = {
        date: '',
        time: ''
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

    const minDate = computed(() => {
      const tomorrow = new Date()
      tomorrow.setDate(tomorrow.getDate() + 1)
      return tomorrow.toISOString().split('T')[0]
    })

    const availableTimes = computed(() => {
      // Generate time slots from 9 AM to 5 PM
      const times = []
      for (let hour = 9; hour < 17; hour++) {
        times.push(`${hour.toString().padStart(2, '0')}:00`)
        times.push(`${hour.toString().padStart(2, '0')}:30`)
      }
      return times
    })

    const fetchBookedSlots = async () => {
      if (!appointmentToReschedule.value || !rescheduleForm.value.date) {
        bookedTimes.value = []
        return
      }
      
      try {
        const response = await patientAPI.getBookedSlots(
          appointmentToReschedule.value.doctor_id, 
          rescheduleForm.value.date
        )
        bookedTimes.value = response.data.data.booked_times
      } catch (error) {
        console.error('Error fetching booked slots:', error)
        bookedTimes.value = []
      }
    }

    // Watch for date changes to fetch booked slots
    watch(() => rescheduleForm.value.date, () => {
      fetchBookedSlots()
    })

    onMounted(() => {
      fetchAppointments()
    })

    return {
      loading,
      upcomingAppointments,
      pastAppointments,
      showRescheduleModal,
      appointmentToReschedule,
      rescheduleForm,
      bookedTimes,
      minDate,
      availableTimes,
      cancelAppointment,
      rescheduleAppointment,
      submitReschedule,
      closeRescheduleModal,
      fetchBookedSlots,
      formatDate,
      formatTime,
      getStatusClass,
      getStatusText
    }
  }
}
</script>
