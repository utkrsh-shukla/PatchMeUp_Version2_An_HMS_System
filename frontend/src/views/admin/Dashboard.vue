<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-speedometer2"></i> Admin Dashboard</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <!-- Welcome Alert -->
      <div class="alert alert-info mb-4">
        <strong>Welcome Admin!</strong> Manage doctors, patients, appointments, and more from this dashboard.
      </div>

      <!-- Top Statistics -->
      <StatsCards :stats="stats" />

      <!-- Registered Doctors -->
      <DoctorsSection :doctors="recentDoctors" />

      <!-- Registered Patients -->
      <PatientsSection :patients="recentPatients" />

      <!-- Upcoming Appointments -->
      <AppointmentsSection :appointments="upcomingAppointments" />

      <!-- Bottom Statistics -->
      <AppointmentStats :stats="stats" />
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import StatsCards from '@/components/admin/StatsCards.vue'
import DoctorsSection from '@/components/admin/DoctorsSection.vue'
import PatientsSection from '@/components/admin/PatientsSection.vue'
import AppointmentsSection from '@/components/admin/AppointmentsSection.vue'
import AppointmentStats from '@/components/admin/AppointmentStats.vue'
import adminAPI from '@/api/admin'

export default {
  name: 'AdminDashboard',
  components: {
    LoadingSpinner,
    StatsCards,
    DoctorsSection,
    PatientsSection,
    AppointmentsSection,
    AppointmentStats
  },
  setup() {
    const loading = ref(true)
    const stats = ref({})
    const recentDoctors = ref([])
    const recentPatients = ref([])
    const upcomingAppointments = ref([])
    
    onMounted(async () => {
      try {
        // Fetch stats
        const statsResponse = await adminAPI.getStats()
        stats.value = statsResponse.data.data
        
        // Fetch recent doctors (limit to 5 for dashboard)
        const doctorsResponse = await adminAPI.getDoctors()
        recentDoctors.value = doctorsResponse.data.data.slice(0, 5)
        
        // Fetch recent patients (limit to 5 for dashboard)
        const patientsResponse = await adminAPI.getPatients()
        recentPatients.value = patientsResponse.data.data.slice(0, 5)
        
        // Fetch upcoming appointments
        const appointmentsResponse = await adminAPI.getUpcomingAppointments()
        upcomingAppointments.value = appointmentsResponse.data.data.slice(0, 5)
        
      } catch (error) {
        console.error('Error fetching admin dashboard data:', error)
      } finally {
        loading.value = false
      }
    })
    
    return {
      loading,
      stats,
      recentDoctors,
      recentPatients,
      upcomingAppointments
    }
  }
}
</script>
