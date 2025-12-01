<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-heart-pulse"></i> Welcome, {{ patientName }}</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Statistics -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card border-start border-danger border-4">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="flex-grow-1">
                  <h1 class="text-danger mb-0">{{ stats.total_appointments || 0 }}</h1>
                  <p class="text-muted mb-0">TOTAL APPOINTMENTS</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card border-start border-danger border-4">
            <div class="card-body">
              <div class="d-flex align-items-center">
                <div class="flex-grow-1">
                  <h1 class="text-danger mb-0">{{ stats.completed_appointments || 0 }}</h1>
                  <p class="text-muted mb-0">COMPLETED VISITS</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body text-center">
              <i class="bi bi-file-medical fs-1 text-primary mb-3"></i>
              <h5>My Treatment History</h5>
              <p class="text-muted">View your complete medical treatment records</p>
              <router-link to="/patient/treatments" class="btn btn-primary">
                <i class="bi bi-eye"></i> View Treatments
              </router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body text-center">
              <i class="bi bi-calendar-plus fs-1 text-success mb-3"></i>
              <h5>Book New Appointment</h5>
              <p class="text-muted">Find doctors and schedule your next visit</p>
              <router-link to="/patient/doctors" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Book Appointment
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Upcoming Appointments -->
      <UpcomingAppointments 
        v-if="upcomingAppointments && upcomingAppointments.length > 0"
        :appointments="upcomingAppointments" 
      />

      <!-- Departments -->
      <DepartmentGrid :departments="departments" />
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import UpcomingAppointments from '@/components/patient/UpcomingAppointments.vue'
import DepartmentGrid from '@/components/patient/DepartmentGrid.vue'

export default {
  name: 'PatientDashboard',
  components: {
    LoadingSpinner,
    UpcomingAppointments,
    DepartmentGrid
  },
  setup() {
    const store = useStore()
    const loading = ref(true)
    
    const stats = computed(() => store.state.patient.stats || {})
    const upcomingAppointments = computed(() => store.state.patient.appointments || [])
    const departments = computed(() => store.state.patient.departments || [])
    const patientName = computed(() => store.state.auth.user?.patient?.name || store.state.auth.user?.name || 'Patient')
    
    onMounted(async () => {
      await store.dispatch('patient/fetchStats')
      await store.dispatch('patient/fetchUpcomingAppointments')
      await store.dispatch('patient/fetchDepartments')
      loading.value = false
    })
    
    return {
      loading,
      stats,
      upcomingAppointments,
      departments,
      patientName
    }
  }
}
</script>
