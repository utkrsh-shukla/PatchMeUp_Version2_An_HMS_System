<template>
  <div class="card">
    <div class="card-header">Patient Information</div>
    <div class="card-body">
      <h5 class="text-danger mb-3">{{ patient.name }}</h5>
      <div class="row">
        <div class="col-md-6">
          <p v-if="showId"><strong>ID:</strong> {{ patient.id }}</p>
          <p v-if="showEmail"><strong>Email:</strong> {{ patient.email }}</p>
          <p v-if="showPhone"><strong>Phone:</strong> {{ patient.phone || 'N/A' }}</p>
          <p v-if="showBloodGroup"><strong>Blood Group:</strong> {{ patient.blood_group || 'N/A' }}</p>
        </div>
        <div class="col-md-6">
          <p v-if="showDateOfBirth && patient.date_of_birth">
            <strong>Date of Birth:</strong> 
            <DateTimeDisplay :date="patient.date_of_birth" format="date" />
          </p>
          <p v-if="showAddress"><strong>Address:</strong> {{ patient.address || 'N/A' }}</p>
          <p v-if="showStatus">
            <strong>Status:</strong>
            <span :class="patient.is_active ? 'badge bg-success' : 'badge bg-secondary'">
              {{ patient.is_active ? 'Active' : 'Inactive' }}
            </span>
          </p>
        </div>
      </div>
      <template v-if="showMedicalHistory && patient.medical_history">
        <hr>
        <p><strong>Medical History:</strong></p>
        <p>{{ patient.medical_history }}</p>
      </template>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
import DateTimeDisplay from './DateTimeDisplay.vue'

export default {
  name: 'PatientInfoCard',
  components: {
    DateTimeDisplay
  },
  props: {
    patient: {
      type: Object,
      required: true
    },
    showId: {
      type: Boolean,
      default: true
    },
    showEmail: {
      type: Boolean,
      default: false
    },
    showPhone: {
      type: Boolean,
      default: true
    },
    showBloodGroup: {
      type: Boolean,
      default: true
    },
    showDateOfBirth: {
      type: Boolean,
      default: true
    },
    showAddress: {
      type: Boolean,
      default: true
    },
    showStatus: {
      type: Boolean,
      default: true
    },
    showMedicalHistory: {
      type: Boolean,
      default: true
    }
  }
}
</script>
