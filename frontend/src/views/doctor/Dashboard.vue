<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-person-badge"></i> Welcome, Dr. {{ doctorName }}</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Statistics -->
      <div class="row mb-4">
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-number">{{ stats.total_appointments || 0 }}</div>
            <div class="stat-label">Total Appointments</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-number">{{ stats.completed_appointments || 0 }}</div>
            <div class="stat-label">Completed</div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-number">{{ stats.upcoming_appointments || 0 }}</div>
            <div class="stat-label">Pending</div>
          </div>
        </div>
      </div>

      <!-- Today's Appointments -->
      <TodaySchedule 
        v-if="todayAppointments && todayAppointments.length > 0"
        :appointments="todayAppointments" 
      />

      <!-- Upcoming Appointments (Next 7 Days) -->
      <DoctorUpcomingAppointments 
        :appointments="upcomingAppointments" 
        @add-treatment="openTreatmentModal"
        @edit-treatment="openEditTreatmentModal"
        @view-history="viewPatientHistory"
      />
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
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import TodaySchedule from '@/components/doctor/TodaySchedule.vue'
import DoctorUpcomingAppointments from '@/components/doctor/DoctorUpcomingAppointments.vue'
import TreatmentForm from '@/components/doctor/TreatmentForm.vue'
import PatientHistory from '@/components/doctor/PatientHistory.vue'
import FormModal from '@/components/common/FormModal.vue'
import doctorAPI from '@/api/doctor'

export default {
  name: 'DoctorDashboard',
  components: {
    LoadingSpinner,
    TodaySchedule,
    DoctorUpcomingAppointments,
    TreatmentForm,
    PatientHistory,
    FormModal
  },
  setup() {
    const store = useStore()
    const loading = ref(true)
    
    const stats = computed(() => store.state.doctor.stats || {})
    const todayAppointments = computed(() => store.state.doctor.todayAppointments || [])
    const upcomingAppointments = computed(() => store.state.doctor.upcomingAppointments || [])
    const doctorName = computed(() => store.state.auth.user?.doctor?.name || 'Doctor')
    
    const showTreatmentModal = ref(false)
    const showHistoryModal = ref(false)
    const selectedAppointment = ref(null)
    const selectedPatientHistory = ref(null)
    const isEditMode = ref(false)
    
    const fetchData = async () => {
      await store.dispatch('doctor/fetchStats')
      await store.dispatch('doctor/fetchTodayAppointments')
      await store.dispatch('doctor/fetchUpcomingAppointments')
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
        await fetchData()
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

    onMounted(async () => {
      await fetchData()
      loading.value = false
    })
    
    return {
      loading,
      stats,
      todayAppointments,
      upcomingAppointments,
      doctorName,
      showTreatmentModal,
      showHistoryModal,
      selectedAppointment,
      selectedPatientHistory,
      isEditMode,
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
