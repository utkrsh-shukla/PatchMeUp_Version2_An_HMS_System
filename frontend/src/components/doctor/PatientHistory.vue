<template>
  <div v-if="patientData">
    <!-- Patient Info -->
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0"><i class="bi bi-person"></i> Patient Information</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">
            <p><strong>Name:</strong> {{ patientData.patient.name }}</p>
            <p><strong>Phone:</strong> {{ patientData.patient.phone || 'N/A' }}</p>
            <p><strong>Blood Group:</strong> {{ patientData.patient.blood_group || 'N/A' }}</p>
          </div>
          <div class="col-md-6">
            <p><strong>Date of Birth:</strong> {{ formatDate(patientData.patient.date_of_birth) || 'N/A' }}</p>
            <p><strong>Address:</strong> {{ patientData.patient.address || 'N/A' }}</p>
          </div>
        </div>
        <div v-if="patientData.patient.medical_history">
          <p><strong>Medical History:</strong></p>
          <p class="text-muted">{{ patientData.patient.medical_history }}</p>
        </div>
      </div>
    </div>

    <!-- Appointment History -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0"><i class="bi bi-clock-history"></i> Previous Appointments</h5>
      </div>
      <div class="card-body">
        <div v-if="patientData.appointments && patientData.appointments.length > 0">
          <div class="accordion" id="appointmentHistory">
            <div 
              v-for="(appointment, index) in patientData.appointments" 
              :key="appointment.id"
              class="accordion-item"
            >
              <h2 class="accordion-header">
                <button 
                  class="accordion-button collapsed" 
                  type="button" 
                  data-bs-toggle="collapse" 
                  :data-bs-target="`#collapse${index}`"
                >
                  <div class="d-flex justify-content-between w-100 me-3">
                    <span>
                      <strong>{{ formatDate(appointment.date) }}</strong> at {{ formatTime(appointment.time) }}
                    </span>
                    <span class="badge bg-success">Completed</span>
                  </div>
                </button>
              </h2>
              <div 
                :id="`collapse${index}`" 
                class="accordion-collapse collapse" 
                data-bs-parent="#appointmentHistory"
              >
                <div class="accordion-body">
                  <div v-if="appointment.treatment">
                    <div class="row">
                      <div class="col-md-12 mb-3">
                        <h6><i class="bi bi-clipboard-pulse"></i> Diagnosis</h6>
                        <p class="mb-2">{{ appointment.treatment.diagnosis }}</p>
                      </div>
                      
                      <div v-if="appointment.treatment.prescription" class="col-md-12 mb-3">
                        <h6><i class="bi bi-capsule"></i> Prescription</h6>
                        <p class="mb-2">{{ appointment.treatment.prescription }}</p>
                      </div>
                      
                      <div v-if="appointment.treatment.notes" class="col-md-12 mb-3">
                        <h6><i class="bi bi-journal-text"></i> Notes</h6>
                        <p class="mb-2">{{ appointment.treatment.notes }}</p>
                      </div>
                    </div>
                    
                    <div v-if="appointment.notes" class="mt-3 pt-3 border-top">
                      <h6><i class="bi bi-chat-text"></i> Appointment Notes</h6>
                      <p class="text-muted mb-0">{{ appointment.notes }}</p>
                    </div>
                  </div>
                  <div v-else>
                    <p class="text-muted">No treatment record available for this appointment.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center text-muted py-4">
          <i class="bi bi-calendar-x fs-1"></i>
          <p class="mt-2">No previous appointments found</p>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-end mt-3">
      <button @click="$emit('close')" class="btn btn-secondary">
        Close
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientHistory',
  props: {
    patientData: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },
    
    formatTime(timeStr) {
      if (!timeStr) return ''
      return new Date(`2000-01-01T${timeStr}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>