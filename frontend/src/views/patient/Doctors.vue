<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-people"></i> Browse Doctors</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Search and Filter Section -->
      <div class="row mb-4">
        <div class="col-md-4">
          <input 
            v-model="searchQuery" 
            @input="searchDoctors"
            type="text" 
            class="form-control" 
            placeholder="Search by doctor name or specialization..."
          />
        </div>
        <div class="col-md-6">
          <select v-model="selectedDepartment" @change="filterDoctors" class="form-select">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">
              {{ dept.name }}
            </option>
          </select>
        </div>
        <div class="col-md-2">
          <button @click="clearFilters" class="btn btn-outline-secondary w-100">
            Clear
          </button>
        </div>
      </div>

      <!-- Doctors Grid -->
      <div class="row">
        <div v-for="doctor in filteredDoctors" :key="doctor.id" class="col-md-6 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title text-primary">{{ doctor.name }}</h5>
              <p class="mb-1"><strong>Specialization:</strong> {{ doctor.specialization }}</p>
              <p class="mb-1"><strong>Department:</strong> {{ doctor.department_name || 'General' }}</p>
              <p class="mb-1"><strong>Experience:</strong> {{ doctor.years_of_experience || 0 }} years</p>
              <p class="mb-3"><strong>Phone:</strong> {{ doctor.phone || 'Not available' }}</p>
              
              <div class="d-flex gap-2">
                <button 
                  @click="viewDetails(doctor)"
                  class="btn btn-outline-info btn-sm"
                >
                  View Details
                </button>
                <button 
                  @click="bookAppointment(doctor)"
                  class="btn btn-primary btn-sm"
                >
                  Book Appointment
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="filteredDoctors.length === 0" class="col-12">
          <div class="text-center text-muted py-5">
            <i class="bi bi-person-x fs-1"></i>
            <p class="mt-2">No doctors found</p>
          </div>
        </div>
      </div>
    </template>

    <!-- Doctor Details Modal -->
    <FormModal
      :show="showDetailsModal"
      :title="selectedDoctor?.name || 'Doctor Details'"
      size="lg"
      @close="closeDetailsModal"
    >
      <div v-if="selectedDoctor">
        <div class="row">
          <div class="col-md-6">
            <p><strong>Name:</strong> {{ selectedDoctor.name }}</p>
            <p><strong>Specialization:</strong> {{ selectedDoctor.specialization }}</p>
            <p><strong>Department:</strong> {{ selectedDoctor.department_name || 'General' }}</p>
          </div>
          <div class="col-md-6">
            <p><strong>Experience:</strong> {{ selectedDoctor.years_of_experience || 0 }} years</p>
            <p><strong>Phone:</strong> {{ selectedDoctor.phone || 'Not available' }}</p>
            <p><strong>Email:</strong> {{ selectedDoctor.email }}</p>
          </div>
        </div>
        
        <div v-if="selectedDoctor.availability" class="mt-4">
          <h6>Available Times:</h6>
          <div class="row">
            <div v-for="(daySlots, date) in selectedDoctor.availability" :key="date" class="col-md-6 mb-2">
              <div v-if="daySlots.slots && daySlots.slots.length > 0">
                <strong>{{ daySlots.day_name }}:</strong>
                <div v-for="slot in daySlots.slots" :key="slot.id" class="ms-2">
                  {{ slot.start_time }} - {{ slot.end_time }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-end gap-2 mt-4">
          <button @click="closeDetailsModal" class="btn btn-secondary">
            Close
          </button>
          <button @click="bookAppointment(selectedDoctor)" class="btn btn-primary">
            Book Appointment
          </button>
        </div>
      </div>
    </FormModal>

    <!-- Book Appointment Modal -->
    <FormModal
      :show="showBookingModal"
      title="Book Appointment"
      @close="closeBookingModal"
    >
      <div v-if="selectedDoctor">
        <p><strong>Doctor:</strong> {{ selectedDoctor.name }}</p>
        <p><strong>Specialization:</strong> {{ selectedDoctor.specialization }}</p>
        
        <form @submit.prevent="submitBooking">
          <div class="mb-3">
            <label for="appointmentDate" class="form-label">Date</label>
            <input 
              id="appointmentDate" 
              v-model="bookingForm.date" 
              type="date" 
              class="form-control" 
              :min="minDate"
              required 
            />
          </div>
          
          <div class="mb-3">
            <label for="appointmentTime" class="form-label">Time</label>
            <select id="appointmentTime" v-model="bookingForm.time" class="form-select" required>
              <option value="">Select Time</option>
              <option 
                v-for="time in availableTimesForDate" 
                :key="time" 
                :value="time"
                :disabled="bookedTimes.includes(time)"
              >
                {{ formatTime(time) }} {{ bookedTimes.includes(time) ? '(Booked)' : '' }}
              </option>
            </select>
          </div>
          
          <div class="mb-3">
            <label for="notes" class="form-label">Notes (Optional)</label>
            <textarea 
              id="notes" 
              v-model="bookingForm.notes" 
              class="form-control" 
              rows="3"
              placeholder="Any specific concerns or notes for the doctor..."
            ></textarea>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button type="button" @click="closeBookingModal" class="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn btn-success">
              Book Appointment
            </button>
          </div>
        </form>
      </div>
      <div v-else>
        <p>Loading doctor information...</p>
        <p>Debug: selectedDoctor is {{ selectedDoctor }}</p>
      </div>
    </FormModal>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import FormModal from '@/components/common/FormModal.vue'
import patientAPI from '@/api/patient'

export default {
  name: 'PatientDoctors',
  components: {
    LoadingSpinner,
    FormModal
  },
  setup() {
    const route = useRoute()
    const loading = ref(true)
    const doctors = ref([])
    const departments = ref([])
    const selectedDepartment = ref('')
    const searchQuery = ref('')
    const showDetailsModal = ref(false)
    const showBookingModal = ref(false)
    const selectedDoctor = ref(null)
    
    const bookingForm = ref({
      date: '',
      time: '',
      notes: ''
    })
    const bookedTimes = ref([])

    const filteredDoctors = computed(() => {
      if (!selectedDepartment.value) {
        return doctors.value
      }
      return doctors.value.filter(doctor => doctor.department_id === selectedDepartment.value)
    })

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

    const availableTimesForDate = computed(() => {
      return availableTimes.value
    })

    const fetchBookedSlots = async () => {
      if (!selectedDoctor.value || !bookingForm.value.date) {
        bookedTimes.value = []
        return
      }
      
      try {
        const response = await patientAPI.getBookedSlots(selectedDoctor.value.id, bookingForm.value.date)
        bookedTimes.value = response.data.data.booked_times
      } catch (error) {
        console.error('Error fetching booked slots:', error)
        bookedTimes.value = []
      }
    }

    const fetchData = async () => {
      try {
        loading.value = true
        
        // Get department from URL parameter
        const departmentParam = route.query.department
        if (departmentParam) {
          selectedDepartment.value = parseInt(departmentParam)
        }
        
        const [doctorsResponse, departmentsResponse] = await Promise.all([
          patientAPI.getDoctors(selectedDepartment.value || null, searchQuery.value || null),
          patientAPI.getDepartments()
        ])
        
        doctors.value = doctorsResponse.data.data
        departments.value = departmentsResponse.data.data
      } catch (error) {
        console.error('Error fetching data:', error)
        alert('Error loading doctors')
      } finally {
        loading.value = false
      }
    }

    const filterDoctors = async () => {
      try {
        const response = await patientAPI.getDoctors(
          selectedDepartment.value || null, 
          searchQuery.value || null
        )
        doctors.value = response.data.data
      } catch (error) {
        console.error('Error filtering doctors:', error)
      }
    }

    const searchDoctors = async () => {
      // Debounce search to avoid too many API calls
      clearTimeout(searchDoctors.timeout)
      searchDoctors.timeout = setTimeout(async () => {
        await filterDoctors()
      }, 300)
    }

    const clearFilters = async () => {
      selectedDepartment.value = ''
      searchQuery.value = ''
      await filterDoctors()
    }

    const viewDetails = async (doctor) => {
      try {
        const response = await patientAPI.getDoctorDetail(doctor.id)
        selectedDoctor.value = response.data.data
        showDetailsModal.value = true
      } catch (error) {
        console.error('Error fetching doctor details:', error)
        alert('Error loading doctor details')
      }
    }

    const bookAppointment = (doctor) => {
      console.log('bookAppointment called with doctor:', doctor)
      selectedDoctor.value = doctor
      bookingForm.value = {
        date: '',
        time: '',
        notes: ''
      }
      
      // Close details modal if it's open
      if (showDetailsModal.value) {
        closeDetailsModal()
      }
      
      showBookingModal.value = true
      console.log('selectedDoctor set to:', selectedDoctor.value)
      console.log('showBookingModal set to:', showBookingModal.value)
    }

    const submitBooking = async () => {
      try {
        await patientAPI.bookAppointment({
          doctor_id: selectedDoctor.value.id,
          date: bookingForm.value.date,
          time: bookingForm.value.time,
          notes: bookingForm.value.notes
        })
        
        closeBookingModal()
        alert('Appointment booked successfully!')
      } catch (error) {
        console.error('Error booking appointment:', error)
        alert(error.response?.data?.error || 'Error booking appointment')
      }
    }

    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedDoctor.value = null
    }

    const closeBookingModal = () => {
      showBookingModal.value = false
      selectedDoctor.value = null
      bookingForm.value = {
        date: '',
        time: '',
        notes: ''
      }
    }

    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      const [hours, minutes] = timeStr.split(':')
      const hour = parseInt(hours)
      const ampm = hour >= 12 ? 'PM' : 'AM'
      const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour
      return `${displayHour}:${minutes} ${ampm}`
    }

    // Watch for date changes to fetch booked slots
    watch(() => bookingForm.value.date, () => {
      fetchBookedSlots()
    })

    onMounted(() => {
      fetchData()
    })

    return {
      loading,
      doctors,
      departments,
      selectedDepartment,
      searchQuery,
      filteredDoctors,
      showDetailsModal,
      showBookingModal,
      selectedDoctor,
      bookingForm,
      bookedTimes,
      minDate,
      availableTimes,
      availableTimesForDate,
      filterDoctors,
      searchDoctors,
      clearFilters,
      fetchBookedSlots,
      viewDetails,
      bookAppointment,
      submitBooking,
      closeDetailsModal,
      closeBookingModal,
      formatTime
    }
  }
}
</script>
