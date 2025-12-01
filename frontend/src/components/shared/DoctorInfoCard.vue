<template>
  <div class="card">
    <div class="card-header">Doctor Information</div>
    <div class="card-body">
      <h5 class="text-danger">{{ doctor.name }}</h5>
      <p><strong>Specialization:</strong> {{ doctor.specialization }}</p>
      <p><strong>Department:</strong> {{ doctor.department_name || 'N/A' }}</p>
      <p v-if="showExperience"><strong>Experience:</strong> {{ doctor.years_of_experience }} years</p>
      <p v-if="showPhone"><strong>Phone:</strong> {{ doctor.phone || 'N/A' }}</p>
      <p v-if="showEmail"><strong>Email:</strong> {{ doctor.email || 'N/A' }}</p>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorInfoCard',
  props: {
    doctor: {
      type: Object,
      required: true
    },
    showExperience: {
      type: Boolean,
      default: true
    },
    showPhone: {
      type: Boolean,
      default: false
    },
    showEmail: {
      type: Boolean,
      default: false
    }
  }
}
</script>
