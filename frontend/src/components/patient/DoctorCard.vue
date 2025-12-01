<template>
  <div class="card feature-card h-100">
    <div class="card-body">
      <h5 class="text-danger">{{ doctor.name }}</h5>
      <p class="mb-2"><strong>Specialization:</strong> {{ doctor.specialization }}</p>
      <p class="mb-2"><strong>Department:</strong> {{ doctor.department_name || 'N/A' }}</p>
      <p class="mb-2"><strong>Experience:</strong> {{ doctor.years_of_experience }} years</p>
      <p class="mb-2"><strong>Phone:</strong> {{ doctor.phone || 'N/A' }}</p>
      <div class="mt-3">
        <slot name="actions">
          <router-link :to="'/patient/doctors/' + doctor.id" class="btn btn-secondary btn-sm me-1">
            View Details
          </router-link>
          <router-link :to="'/patient/book-appointment/' + doctor.id" class="btn btn-primary btn-sm">
            Book Appointment
          </router-link>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorCard',
  props: {
    doctor: { type: Object, required: true }
  }
}
</script>
