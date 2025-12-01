<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-calendar-check"></i> My Appointments</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Filter Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <button 
            class="nav-link" 
            :class="{ active: activeTab === 'today' }"
            @click="activeTab = 'today'"
          >
            <i class="bi bi-calendar-day"></i> Today ({{ todayAppointments.length }})
          </button>
        </li>
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

      <!-- Today's Appointments -->
      <div v-if="activeTab === 'today'">
        <AppointmentsList 
          :appointments="todayAppointments"
          title="Today's Appointments"
          :show-actions="true"
          @complete="handleComplete"
          @cancel="handleCancel"
          @add-treatment="openTreatmentModal"
          @edit-treatment="openEditTreatmentModal"
          @view-history="viewPatientHistory"
        />
      </div>

      <!-- Upcoming Appointments -->
      <div v-if="activeTab === 'upcoming'">
        <AppointmentsList 
          :appointments="upcomingAppointments"
          title="Upcoming Appointments"
          :show-actions="true"
          @complete="handleComplete"
          @cancel="handleCancel"
          @add-treatment="openTreatmentModal"
          @edit-treatment="openEditTreatmentModal"
          @view-history="viewPatientHistory"
        />
      </div>

      <!-- All Appointments -->
      <div v-if="activeTab === 'all'">
        <AppointmentsList 
          :appointments="allAppointments"
          title="All Appointments"
          :show-actions="true"
          @complete="handleComplete"
          @cancel="handleCancel"
          @add-treatment="openTreatmentModal"
          @edit-treatment="openEditTreatmentModal"
          @view-history="viewPatientHistory"
        />
      </div>
    </template>

    <!-- Treatment Modal -->
    <FormModal
      :show="showTreatmentModal"
      :title="isEditMode ? 'Edit Treatment Record' : 'Add Treatment Record'"
      size="lg"
      @close="closeTreatmentModal"
    >
      <TreatmentForm
        :appointment="selectedAppointment"
        :is-edit="isEditMode"
        @submit="handleTreatmentSubmit"
        @cancel="closeTreatmentModal"
      />
    </FormModal>

    <!-- Patient History Modal -->
    <FormModal
      :show="showHistoryModal"
      title="Patient Medical History"
      size="xl"
      @close="closeHistoryModal"
    >
      <PatientHistory
        :patient-data="selectedPatientHistory"
        @close="closeHistoryModal"
      />
    </FormModal>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import AppointmentsList from '@/components/doctor/AppointmentsList.vue'
import TreatmentForm from '@/components/doctor/TreatmentForm.vue'
import PatientHistory from '@/components/doctor/PatientHistory.vue'
import FormModal from '@/components/common/FormModal.vue'
import doctorAPI from '@/api/doctor'

export default {
  name: 'DoctorAppointments',
  components: {
    LoadingSpinner,
    AppointmentsList,
    TreatmentForm,
    PatientHistory,
    FormModal
  },
  setup() {
    const loading = ref(true)
    const activeTab = ref('today')
    const todayAppointments = ref([])
    const upcomingAppointments = ref([])
    const allAppointments = ref([])
    const showTreatmentModal = ref(false)
    const showHistoryModal = ref(false)
    const selectedAppointment = ref(null)
    const selectedPatientHistory = ref(null)
    const isEditMode = ref(false)

    const fetchAppointments = async () => {
      try {
        loading.value = true
        
        // Fetch all appointment types
        const [todayResponse, upcomingResponse, allResponse] = await Promise.all([
          doctorAPI.getTodayAppointments(),
          doctorAPI.getUpcomingAppointments(),
          doctorAPI.getAllAppointments()
        ])

        todayAppointments.value = todayResponse.data.data
        upcomingAppointments.value = upcomingResponse.data.data
        allAppointments.value = allResponse.data.data

      } catch (error) {
        console.error('Error fetching appointments:', error)
        alert('Error loading appointments')
      } finally {
        loading.value = false
      }
    }

    const handleComplete = async (appointmentId) => {
      if (confirm('Mark this appointment as completed?')) {
        try {
          await doctorAPI.completeAppointment(appointmentId)
          await fetchAppointments()
          alert('Appointment marked as completed')
        } catch (error) {
          console.error('Error completing appointment:', error)
          alert('Error completing appointment')
        }
      }
    }

    const handleCancel = async (appointmentId) => {
      if (confirm('Cancel this appointment?')) {
        try {
          await doctorAPI.cancelAppointment(appointmentId)
          await fetchAppointments()
          alert('Appointment cancelled')
        } catch (error) {
          console.error('Error cancelling appointment:', error)
          alert('Error cancelling appointment')
        }
      }
    }

    const openTreatmentModal = (appointment) => {
      selectedAppointment.value = appointment
      isEditMode.value = false
      showTreatmentModal.value = true
    }

    const openEditTreatmentModal = (appointment) => {
      selectedAppointment.value = appointment
      isEditMode.value = true
      showTreatmentModal.value = true
    }

    const closeTreatmentModal = () => {
      showTreatmentModal.value = false
      selectedAppointment.value = null
      isEditMode.value = false
    }

    const handleTreatmentSubmit = async (treatmentData) => {
      try {
        if (isEditMode.value) {
          await doctorAPI.updateTreatment(selectedAppointment.value.id, treatmentData)
          alert('Treatment record updated successfully')
        } else {
          await doctorAPI.addTreatment(selectedAppointment.value.id, treatmentData)
          alert('Treatment record added successfully')
        }
        await fetchAppointments()
        closeTreatmentModal()
      } catch (error) {
        console.error('Error saving treatment:', error)
        alert(`Error ${isEditMode.value ? 'updating' : 'adding'} treatment record`)
      }
    }

    const viewPatientHistory = async (patientId) => {
      try {
        const response = await doctorAPI.getPatientHistory(patientId)
        selectedPatientHistory.value = response.data.data
        showHistoryModal.value = true
      } catch (error) {
        console.error('Error fetching patient history:', error)
        alert('Error loading patient history')
      }
    }

    const closeHistoryModal = () => {
      showHistoryModal.value = false
      selectedPatientHistory.value = null
    }

    onMounted(() => {
      fetchAppointments()
    })

    return {
      loading,
      activeTab,
      todayAppointments,
      upcomingAppointments,
      allAppointments,
      showTreatmentModal,
      showHistoryModal,
      selectedAppointment,
      selectedPatientHistory,
      isEditMode,
      handleComplete,
      handleCancel,
      openTreatmentModal,
      openEditTreatmentModal,
      closeTreatmentModal,
      handleTreatmentSubmit,
      viewPatientHistory,
      closeHistoryModal
    }
  }
}
</script>
