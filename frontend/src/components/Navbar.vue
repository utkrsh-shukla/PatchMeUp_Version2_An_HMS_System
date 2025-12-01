<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <i class="bi bi-hospital"></i> PatchMeUp Hospital
      </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <template v-if="!isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
          </template>
          
          <template v-else>
            <!-- Admin Menu -->
            <template v-if="isAdmin">
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/doctors">Doctors</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/patients">Patients</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin/search">Search</router-link>
              </li>
            </template>
            
            <!-- Doctor Menu -->
            <template v-if="isDoctor">
              <li class="nav-item">
                <router-link class="nav-link" to="/doctor/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/doctor/appointments">Appointments</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/doctor/availability">Availability</router-link>
              </li>
            </template>
            
            <!-- Patient Menu -->
            <template v-if="isPatient">
              <li class="nav-item">
                <router-link class="nav-link" to="/patient/dashboard">Dashboard</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/patient/doctors">Doctors</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/patient/appointments">My Appointments</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/patient/treatments">My Treatments</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/patient/profile">Profile</router-link>
              </li>
            </template>
            
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="handleLogout">Logout</a>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const store = useStore()
    const router = useRouter()

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const currentUser = computed(() => store.getters['auth/currentUser'])
    const isAdmin = computed(() => store.getters['auth/isAdmin'])
    const isDoctor = computed(() => store.getters['auth/isDoctor'])
    const isPatient = computed(() => store.getters['auth/isPatient'])

    const handleLogout = () => {
      store.dispatch('auth/logout')
      router.push('/login')
    }

    return {
      isAuthenticated,
      currentUser,
      isAdmin,
      isDoctor,
      isPatient,
      handleLogout
    }
  }
}
</script>

