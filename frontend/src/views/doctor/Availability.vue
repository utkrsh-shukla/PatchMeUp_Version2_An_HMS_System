<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2><i class="bi bi-calendar-week"></i> My Availability Schedule</h2>
      <button @click="showAddModal = true" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Add Time Slot
      </button>
    </div>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Weekly Schedule -->
      <div v-for="(day, dayIndex) in daysOfWeek" :key="dayIndex" class="mb-4">
        <h5 class="text-muted mb-3">{{ day }}</h5>
        
        <div v-if="getAvailabilityForDay(dayIndex).length > 0">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in getAvailabilityForDay(dayIndex)" :key="slot.id">
                  <td>{{ formatTime(slot.start_time) }}</td>
                  <td>{{ formatTime(slot.end_time) }}</td>
                  <td>
                    <span class="badge bg-success">Available</span>
                  </td>
                  <td>
                    <button 
                      @click="deleteSlot(slot.id)"
                      class="btn btn-sm btn-danger"
                      title="Delete this time slot"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div v-else class="text-muted py-3">
          No availability set for this day
        </div>
        
        <hr v-if="dayIndex < daysOfWeek.length - 1" class="my-4">
      </div>
    </template>

    <!-- Add Time Slot Modal -->
    <FormModal
      :show="showAddModal"
      title="Add Time Slot"
      @close="closeAddModal"
    >
      <form @submit.prevent="addAvailability">
        <div class="mb-3">
          <label for="dayOfWeek" class="form-label">Day of Week</label>
          <select id="dayOfWeek" v-model="newSlot.day_of_week" class="form-select" required>
            <option value="">Select Day</option>
            <option v-for="(day, index) in daysOfWeek" :key="index" :value="index">
              {{ day }}
            </option>
          </select>
        </div>
        
        <div class="row">
          <div class="col-md-6">
            <label for="startTime" class="form-label">Start Time</label>
            <input 
              id="startTime" 
              v-model="newSlot.start_time" 
              type="time" 
              class="form-control" 
              required 
            />
          </div>
          <div class="col-md-6">
            <label for="endTime" class="form-label">End Time</label>
            <input 
              id="endTime" 
              v-model="newSlot.end_time" 
              type="time" 
              class="form-control" 
              required 
            />
          </div>
        </div>

        <div class="d-flex justify-content-end gap-2 mt-4">
          <button type="button" @click="closeAddModal" class="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            <i class="bi bi-plus"></i> Add Time Slot
          </button>
        </div>
      </form>
    </FormModal>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import FormModal from '@/components/common/FormModal.vue'
import doctorAPI from '@/api/doctor'

export default {
  name: 'DoctorAvailability',
  components: {
    LoadingSpinner,
    FormModal
  },
  setup() {
    const loading = ref(true)
    const availability = ref({})
    const showAddModal = ref(false)
    const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    const newSlot = ref({
      day_of_week: '',
      start_time: '',
      end_time: ''
    })

    const fetchAvailability = async () => {
      try {
        loading.value = true
        const response = await doctorAPI.getAvailability()
        availability.value = response.data.data
      } catch (error) {
        console.error('Error fetching availability:', error)
        alert('Error loading availability schedule')
      } finally {
        loading.value = false
      }
    }

    const getAvailabilityForDay = (dayIndex) => {
      return availability.value[dayIndex] || []
    }

    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      const [hours, minutes] = timeStr.split(':')
      const hour = parseInt(hours)
      const ampm = hour >= 12 ? 'PM' : 'AM'
      const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour
      return `${displayHour.toString().padStart(2, '0')}:${minutes} ${ampm}`
    }

    const addAvailability = async () => {
      if (!newSlot.value.day_of_week || !newSlot.value.start_time || !newSlot.value.end_time) {
        alert('Please fill in all fields')
        return
      }

      if (newSlot.value.start_time >= newSlot.value.end_time) {
        alert('End time must be after start time')
        return
      }

      try {
        await doctorAPI.addAvailability({
          day_of_week: parseInt(newSlot.value.day_of_week),
          start_time: newSlot.value.start_time,
          end_time: newSlot.value.end_time
        })

        closeAddModal()
        await fetchAvailability()
        alert('Time slot added successfully')
      } catch (error) {
        console.error('Error adding availability:', error)
        alert('Error adding time slot')
      }
    }

    const deleteSlot = async (slotId) => {
      if (confirm('Delete this time slot?')) {
        try {
          await doctorAPI.deleteAvailability(slotId)
          await fetchAvailability()
          alert('Time slot deleted')
        } catch (error) {
          console.error('Error deleting availability:', error)
          alert('Error deleting time slot')
        }
      }
    }

    const closeAddModal = () => {
      showAddModal.value = false
      newSlot.value = {
        day_of_week: '',
        start_time: '',
        end_time: ''
      }
    }

    onMounted(() => {
      fetchAvailability()
    })

    return {
      loading,
      availability,
      showAddModal,
      daysOfWeek,
      newSlot,
      getAvailabilityForDay,
      formatTime,
      addAvailability,
      deleteSlot,
      closeAddModal
    }
  }
}
</script>
