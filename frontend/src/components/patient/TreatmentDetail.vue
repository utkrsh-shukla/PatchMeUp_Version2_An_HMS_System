<template>
  <div class="treatment-detail">
    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="treatment">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-md-8">
          <h4 class="mb-1">
            <i class="bi bi-file-medical text-primary me-2"></i>
            Treatment Record
          </h4>
          <p class="text-muted mb-0">{{ formatDate(treatment.date) }} at {{ formatTime(treatment.time) }}</p>
        </div>
        <div class="col-md-4 text-end">
          <span class="badge bg-success fs-6">Completed</span>
        </div>
      </div>
      
      <!-- Doctor Information -->
      <div class="card mb-4">
        <div class="card-header">
          <h6 class="mb-0"><i class="bi bi-person-badge me-2"></i>Doctor Information</h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <strong>{{ treatment.doctor.name }}</strong>
              <br>
              <span class="text-muted">{{ treatment.doctor.specialization }}</span>
              <br>
              <span class="text-muted">{{ treatment.doctor.department }}</span>
            </div>
            <div class="col-md-6">
              <div v-if="treatment.doctor.phone">
                <strong>Phone:</strong> {{ treatment.doctor.phone }}
              </div>
              <div v-if="treatment.doctor.years_of_experience">
                <strong>Experience:</strong> {{ treatment.doctor.years_of_experience }} years
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Treatment Details -->
      <div class="card mb-4">
        <div class="card-header">
          <h6 class="mb-0"><i class="bi bi-clipboard-pulse me-2"></i>Treatment Details</h6>
        </div>
        <div class="card-body">
          <!-- Diagnosis -->
          <div class="mb-3">
            <label class="form-label fw-bold">Diagnosis</label>
            <div class="p-3 bg-light rounded">
              {{ treatment.treatment.diagnosis }}
            </div>
          </div>
          
          <!-- Prescription -->
          <div class="mb-3" v-if="treatment.treatment.prescription">
            <label class="form-label fw-bold">Prescription</label>
            <div class="p-3 bg-light rounded">
              {{ treatment.treatment.prescription }}
            </div>
          </div>
          <div class="mb-3" v-else>
            <label class="form-label fw-bold">Prescription</label>
            <div class="p-3 bg-light rounded text-muted">
              No prescription provided
            </div>
          </div>
          
          <!-- Treatment Notes -->
          <div class="mb-3" v-if="treatment.treatment.notes">
            <label class="form-label fw-bold">Additional Notes</label>
            <div class="p-3 bg-light rounded">
              {{ treatment.treatment.notes }}
            </div>
          </div>
          
          <!-- Appointment Notes -->
          <div class="mb-3" v-if="treatment.appointment_notes">
            <label class="form-label fw-bold">Appointment Notes</label>
            <div class="p-3 bg-light rounded">
              {{ treatment.appointment_notes }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Timestamps -->
      <div class="card">
        <div class="card-header">
          <h6 class="mb-0"><i class="bi bi-clock-history me-2"></i>Record Information</h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <strong>Created:</strong> {{ formatDateTime(treatment.treatment.created_at) }}
            </div>
            <div class="col-md-6" v-if="treatment.treatment.updated_at !== treatment.treatment.created_at">
              <strong>Last Updated:</strong> {{ formatDateTime(treatment.treatment.updated_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-4">
      <i class="bi bi-exclamation-triangle fs-1 text-warning mb-3 d-block"></i>
      <h6>Treatment Not Found</h6>
      <p class="text-muted">The requested treatment record could not be found.</p>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import patientAPI from '@/api/patient'

export default {
  name: 'TreatmentDetail',
  props: {
    treatmentId: {
      type: Number,
      default: null
    },
    treatmentData: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const loading = ref(false)
    const treatment = ref(null)
    
    const fetchTreatmentDetail = async (id) => {
      if (!id) return
      
      try {
        loading.value = true
        const response = await patientAPI.getTreatmentDetail(id)
        treatment.value = response.data.data
      } catch (error) {
        console.error('Error fetching treatment detail:', error)
        treatment.value = null
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    const formatTime = (timeStr) => {
      return new Date(`2000-01-01T${timeStr}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const formatDateTime = (dateTimeStr) => {
      if (!dateTimeStr) return 'N/A'
      return new Date(dateTimeStr).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Watch for changes in treatmentId or treatmentData
    watch(() => props.treatmentId, (newId) => {
      if (newId) {
        fetchTreatmentDetail(newId)
      }
    }, { immediate: true })
    
    watch(() => props.treatmentData, (newData) => {
      if (newData) {
        treatment.value = newData
      }
    }, { immediate: true })
    
    return {
      loading,
      treatment,
      formatDate,
      formatTime,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.treatment-detail {
  max-width: 800px;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.form-label {
  color: #495057;
  margin-bottom: 0.5rem;
}
</style>