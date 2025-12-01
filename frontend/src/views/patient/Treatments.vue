<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2><i class="bi bi-file-medical"></i> My Treatments</h2>
      <button 
        @click="exportTreatments" 
        class="btn btn-outline-success"
        :disabled="exportLoading"
      >
        <i class="bi bi-download"></i>
        {{ exportLoading ? 'Exporting...' : 'Export CSV' }}
      </button>
    </div>

    <!-- Treatment History -->
    <TreatmentHistory @view-detail="openTreatmentDetail" />

    <!-- Treatment Detail Modal -->
    <FormModal
      :show="showDetailModal"
      title="Treatment Details"
      size="xl"
      @close="closeDetailModal"
    >
      <TreatmentDetail :treatment-data="selectedTreatment" />
    </FormModal>
  </div>
</template>

<script>
import { ref } from 'vue'
import TreatmentHistory from '@/components/patient/TreatmentHistory.vue'
import TreatmentDetail from '@/components/patient/TreatmentDetail.vue'
import FormModal from '@/components/common/FormModal.vue'
import patientAPI from '@/api/patient'

export default {
  name: 'PatientTreatments',
  components: {
    TreatmentHistory,
    TreatmentDetail,
    FormModal
  },
  setup() {
    const showDetailModal = ref(false)
    const selectedTreatment = ref(null)
    const exportLoading = ref(false)
    
    const openTreatmentDetail = (treatment) => {
      selectedTreatment.value = treatment
      showDetailModal.value = true
    }
    
    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedTreatment.value = null
    }
    
    const exportTreatments = async () => {
      try {
        exportLoading.value = true
        const response = await patientAPI.exportTreatments()
        
        alert('Export started! Please wait while we generate your treatment history...')
        
        // Poll for job status and download when ready
        if (response.data.data.task_id) {
          pollJobStatus(response.data.data.task_id)
        }
      } catch (error) {
        console.error('Error starting export:', error)
        alert('Error starting export. Please try again.')
        exportLoading.value = false
      }
    }
    
    const pollJobStatus = async (taskId) => {
      try {
        const response = await patientAPI.getJobStatus(taskId)
        const jobData = response.data.data
        
        if (jobData.state === 'SUCCESS') {
          exportLoading.value = false
          const filename = jobData.result.filename
          
          // Trigger download
          if (filename) {
            downloadFile(filename)
            alert('Export completed! Your CSV file is being downloaded.')
          } else {
            alert('Export completed! Check Google Chat for the notification.')
          }
        } else if (jobData.state === 'FAILURE') {
          exportLoading.value = false
          alert('Export failed: ' + jobData.error)
        } else if (jobData.state === 'PENDING' || jobData.state === 'PROGRESS') {
          // Poll again in 3 seconds
          setTimeout(() => pollJobStatus(taskId), 3000)
        }
      } catch (error) {
        console.error('Error checking job status:', error)
        exportLoading.value = false
      }
    }
    
    const downloadFile = async (filename) => {
      try {
        const downloadUrl = `/api/patient/download-export/${filename}`
        const token = localStorage.getItem('access_token')
        const response = await fetch(downloadUrl, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = filename
          link.style.display = 'none'
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        } else {
          throw new Error('Download failed')
        }
      } catch (error) {
        console.error('Error downloading file:', error)
        alert('Error downloading file. Please try again.')
      }
    }
    
    return {
      showDetailModal,
      selectedTreatment,
      exportLoading,
      openTreatmentDetail,
      closeDetailModal,
      exportTreatments
    }
  }
}
</script>