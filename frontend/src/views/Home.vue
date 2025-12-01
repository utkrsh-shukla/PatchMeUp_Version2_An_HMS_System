<template>
  <!-- Hero Section -->
  <div class="hero-section text-center">
    <div class="container">
      <h1 class="hero-title">Welcome to PatchMeUp Hospital Management System</h1>
      <p class="hero-subtitle mt-3">
        PatchMeUp Hospital's HMS, A comprehensive hospital management system for efficient healthcare delivery. Developed by Yours Truly Utkarsh Shukla (utkrsh313@gmail.com)
      </p>
      <div class="mt-4">
        <router-link v-if="!isAuthenticated" to="/login" class="btn btn-primary btn-lg me-3">
          <i class="bi bi-box-arrow-in-right"></i> Login to Your Account
        </router-link>
        <router-link v-if="!isAuthenticated" to="/register" class="btn btn-secondary btn-lg">
          <i class="bi bi-calendar-check"></i> Book Your Appointment
        </router-link>
        <router-link v-if="isAuthenticated && isAdmin" to="/admin/dashboard" class="btn btn-primary btn-lg">
          <i class="bi bi-speedometer2"></i> Go to Dashboard
        </router-link>
        <router-link v-if="isAuthenticated && isDoctor" to="/doctor/dashboard" class="btn btn-primary btn-lg">
          <i class="bi bi-calendar-heart"></i> Go to Dashboard
        </router-link>
        <router-link v-if="isAuthenticated && isPatient" to="/patient/dashboard" class="btn btn-primary btn-lg">
          <i class="bi bi-house-heart"></i> Go to Dashboard
        </router-link>
      </div>
    </div>
  </div>

  <!-- Features Section -->
  <div class="container my-5">
    <h2 class="text-center mb-5" style="color: var(--primary-red); font-weight: bold;">Our Core Features</h2>

    <div class="row">
      <!-- Admin Dashboard Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-shield-check feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Admin Dashboard</h4>
            <p class="text-muted">
              Add Doctors, manage doctors and patients, track appointments, search patients and doctors,
              and maintain complete hospital records.
            </p>
          </div>
        </div>
      </div>

      <!-- Doctor Dashboard Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-person-badge feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Doctor Dashboard</h4>
            <p class="text-muted">
              View upcoming appointments for the next 7 days, manage patient records,
              and update your availability schedule.
            </p>
          </div>
        </div>
      </div>

      <!-- Patient Dashboard Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-heart-pulse feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Patient Dashboard</h4>
            <p class="text-muted">
              Browse doctors by specialization, book appointments, view treatment history,
              and manage your profile.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <!-- Intelligent Scheduling Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-calendar2-week feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Intelligent Scheduling</h4>
            <p class="text-muted">
              Prevent double booking with our intelligent appointment scheduler
              and real-time availability updates.
            </p>
          </div>
        </div>
      </div>

      <!-- Complete Medical Records Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-file-medical feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Complete Medical Records</h4>
            <p class="text-muted">
              Comprehensive treatment records including diagnosis, prescriptions,
              and complete patient medical history.
            </p>
          </div>
        </div>
      </div>

      <!-- Easy Search Feature -->
      <div class="col-md-4 mb-4">
        <div class="card feature-card h-100 text-center p-4">
          <div class="card-body">
            <i class="bi bi-search feature-icon"></i>
            <h4 class="mt-3" style="color: var(--primary-red);">Easy Search</h4>
            <p class="text-muted">
              Find doctors by specialization or name, access patient records instantly,
              and navigate with ease.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const isAdmin = computed(() => store.getters['auth/isAdmin'])
    const isDoctor = computed(() => store.getters['auth/isDoctor'])
    const isPatient = computed(() => store.getters['auth/isPatient'])
    
    return {
      isAuthenticated,
      isAdmin,
      isDoctor,
      isPatient
    }
  }
}
</script>

