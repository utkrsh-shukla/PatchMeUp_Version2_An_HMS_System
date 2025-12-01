<template>
  <div class="card">
    <div class="card-header">
      <h5 class="mb-0">
        <i class="bi bi-file-medical"></i> My Treatment History
        <span class="badge bg-primary ms-2">{{ treatments.length }} Records</span>
      </h5>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <div v-else-if="treatments.length === 0" class="text-center py-4 text-muted">
        <i class="bi bi-file-medical-fill fs-1 mb-3 d-block"></i>
        <h6>No Treatment Records Found</h6>
        <p>You don't have any completed treatments yet.</p>
      </div>
      
      <div v-else>
        <div class="row">
          <div class="col-md-6 mb-3" v-for="treatment in treatments" :key="treatment.id">
            <div class="card h-100 treatment-card" @click="viewTreatmentDetail(treatment)">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h6 class="card-title mb-0">
                    <i class="bi bi-calendar-check text-success me-1"></i>
                    {{ formatDate(treatment.date) }}
                  </h6>
                  <small class="text-muted">{{ formatTime(treatment.time) }}</small>
                </div>
                
                <div class="mb-2">
                  <strong class="text-primary">Dr. {{ treatment.doctor.name }}</strong>
                  <br>
                  <small class="text-muted">
                    {{ treatment.doctor.specialization }}
                    <span v-if="treatment.doctor.department"> • {{ treatment.doctor.department }}</span>
                  </small>
                </div>
                
                <div class="mb-2">
                  <strong>Diagnosis:</strong>
                  <p class="mb-1 text-truncate">{{ treatment.treatment.diagnosis }}</p>
                </div>
                
                <div v-if="treatment.treatment.prescription" class="mb-2">
                  <strong>Prescription:</strong>
                  <p class="mb-1 text-truncate text-muted">{{ treatment.treatment.prescription }}</p>
                </div>
                
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    <i class="bi bi-clock"></i> 
                    {{ formatDateTime(treatment.treatment.created_at) }}
                  </small>
                  <button class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-eye"></i> View Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import patientAPI from '@/api/patient'

export default {
  name: 'TreatmentHistory',
  emits: ['view-detail'],
  setup(props, { emit }) {
    const loading = ref(true)
    const treatments = ref([])
    
    const fetchTreatmentHistory = async () => {
      try {
        loading.value = true
        const response = await patientAPI.getTreatmentHistory()
        treatments.value = response.data.data.treatments
      } catch (error) {
        console.error('Error fetching treatment history:', error)
        alert('Error loading treatment history')
      } finally {
        loading.value = false
      }
    }
    
    const viewTreatmentDetail = (treatment) => {
      emit('view-detail', treatment)
    }
    
    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('en-US', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
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
      return new Date(dateTimeStr).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    }
    
    onMounted(() => {
      fetchTreatmentHistory()
    })
    
    return {
      loading,
      treatments,
      viewTreatmentDetail,
      formatDate,
      formatTime,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.treatment-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.treatment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.text-truncate {
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>