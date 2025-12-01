<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-person-circle"></i> My Profile</h2>

    <LoadingSpinner v-if="loading" />
    
    <template v-else>
      <div class="row">
        <!-- Profile Information -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Personal Information</h5>
              <button 
                v-if="!editMode" 
                @click="editMode = true" 
                class="btn btn-primary btn-sm"
              >
                <i class="bi bi-pencil"></i> Edit Profile
              </button>
            </div>
            <div class="card-body">
              <form v-if="editMode" @submit.prevent="updateProfile">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="name" class="form-label">Full Name *</label>
                    <input 
                      id="name" 
                      v-model="form.name" 
                      type="text" 
                      class="form-control" 
                      required 
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input 
                      id="email" 
                      :value="profile.email" 
                      type="email" 
                      class="form-control" 
                      disabled 
                    />
                    <small class="text-muted">Email cannot be changed</small>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="phone" class="form-label">Phone Number</label>
                    <input 
                      id="phone" 
                      v-model="form.phone" 
                      type="tel" 
                      class="form-control" 
                    />
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="dateOfBirth" class="form-label">Date of Birth</label>
                    <input 
                      id="dateOfBirth" 
                      v-model="form.date_of_birth" 
                      type="date" 
                      class="form-control" 
                    />
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="bloodGroup" class="form-label">Blood Group</label>
                    <select id="bloodGroup" v-model="form.blood_group" class="form-select">
                      <option value="">Select Blood Group</option>
                      <option value="A+">A+</option>
                      <option value="A-">A-</option>
                      <option value="B+">B+</option>
                      <option value="B-">B-</option>
                      <option value="AB+">AB+</option>
                      <option value="AB-">AB-</option>
                      <option value="O+">O+</option>
                      <option value="O-">O-</option>
                    </select>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="address" class="form-label">Address</label>
                  <textarea 
                    id="address" 
                    v-model="form.address" 
                    class="form-control" 
                    rows="3"
                  ></textarea>
                </div>

                <div class="mb-3">
                  <label for="medicalHistory" class="form-label">Medical History</label>
                  <textarea 
                    id="medicalHistory" 
                    v-model="form.medical_history" 
                    class="form-control" 
                    rows="4"
                    placeholder="Any allergies, chronic conditions, previous surgeries, etc."
                  ></textarea>
                </div>

                <div class="d-flex gap-2">
                  <button type="submit" class="btn btn-success">
                    <i class="bi bi-check-circle"></i> Save Changes
                  </button>
                  <button type="button" @click="cancelEdit" class="btn btn-secondary">
                    Cancel
                  </button>
                </div>
              </form>

              <!-- View Mode -->
              <div v-else>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <strong>Full Name:</strong>
                    <p class="mb-0">{{ profile.name || 'Not provided' }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <strong>Email:</strong>
                    <p class="mb-0">{{ profile.email }}</p>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <strong>Phone:</strong>
                    <p class="mb-0">{{ profile.phone || 'Not provided' }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <strong>Date of Birth:</strong>
                    <p class="mb-0">{{ formatDate(profile.date_of_birth) || 'Not provided' }}</p>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <strong>Blood Group:</strong>
                    <p class="mb-0">{{ profile.blood_group || 'Not provided' }}</p>
                  </div>
                  <div class="col-md-6 mb-3">
                    <strong>Age:</strong>
                    <p class="mb-0">{{ calculateAge(profile.date_of_birth) || 'Not available' }}</p>
                  </div>
                </div>

                <div class="mb-3">
                  <strong>Address:</strong>
                  <p class="mb-0">{{ profile.address || 'Not provided' }}</p>
                </div>

                <div class="mb-3">
                  <strong>Medical History:</strong>
                  <p class="mb-0">{{ profile.medical_history || 'No medical history recorded' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="col-lg-4">
          <div class="card mb-4">
            <div class="card-header">
              <h5 class="mb-0">Account Summary</h5>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between mb-2">
                <span>Total Appointments:</span>
                <strong>{{ stats.total_appointments || 0 }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Completed Visits:</span>
                <strong>{{ stats.completed_appointments || 0 }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Upcoming Appointments:</span>
                <strong>{{ stats.upcoming_appointments || 0 }}</strong>
              </div>
              <hr>
              <div class="d-flex justify-content-between">
                <span>Member Since:</span>
                <strong>{{ formatDate(profile.created_at) || 'Recently' }}</strong>
              </div>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <router-link to="/patient/appointments" class="btn btn-outline-primary">
                  <i class="bi bi-calendar-check"></i> My Appointments
                </router-link>
                <router-link to="/patient/doctors" class="btn btn-outline-info">
                  <i class="bi bi-search"></i> Find Doctors
                </router-link>
                <button 
                  @click="exportTreatments" 
                  class="btn btn-outline-success"
                  :disabled="exportLoading"
                >
                  <span v-if="exportLoading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-download"></i> 
                  {{ exportLoading ? 'Exporting...' : 'Export Treatment History' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import patientAPI from '@/api/patient'

export default {
  name: 'PatientProfile',
  components: {
    LoadingSpinner
  },
  setup() {
    const loading = ref(true)
    const editMode = ref(false)
    const exportLoading = ref(false)
    const profile = ref({})
    const stats = ref({})
    const form = ref({
      name: '',
      phone: '',
      date_of_birth: '',
      blood_group: '',
      address: '',
      medical_history: ''
    })

    const fetchProfile = async () => {
      try {
        loading.value = true
        const [profileResponse, statsResponse] = await Promise.all([
          patientAPI.getProfile(),
          patientAPI.getStats()
        ])
        
        profile.value = profileResponse.data.data
        stats.value = statsResponse.data.data
        
        // Populate form with current data
        form.value = {
          name: profile.value.name || '',
          phone: profile.value.phone || '',
          date_of_birth: profile.value.date_of_birth || '',
          blood_group: profile.value.blood_group || '',
          address: profile.value.address || '',
          medical_history: profile.value.medical_history || ''
        }
      } catch (error) {
        console.error('Error fetching profile:', error)
        alert('Error loading profile')
      } finally {
        loading.value = false
      }
    }

    const updateProfile = async () => {
      try {
        await patientAPI.updateProfile(form.value)
        await fetchProfile()
        editMode.value = false
        alert('Profile updated successfully')
      } catch (error) {
        console.error('Error updating profile:', error)
        alert('Error updating profile')
      }
    }

    const cancelEdit = () => {
      editMode.value = false
      // Reset form to original values
      form.value = {
        name: profile.value.name || '',
        phone: profile.value.phone || '',
        date_of_birth: profile.value.date_of_birth || '',
        blood_group: profile.value.blood_group || '',
        address: profile.value.address || '',
        medical_history: profile.value.medical_history || ''
      }
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return null
      return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const calculateAge = (dateOfBirth) => {
      if (!dateOfBirth) return null
      const today = new Date()
      const birthDate = new Date(dateOfBirth)
      let age = today.getFullYear() - birthDate.getFullYear()
      const monthDiff = today.getMonth() - birthDate.getMonth()
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--
      }
      
      return age + ' years'
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
            alert('Export completed! Your CSV file is being downloaded. You will also receive a Google Chat notification.')
          } else {
            alert('Export completed! Check Google Chat for the notification with your treatment history details.')
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
      }
    }

    const downloadFile = async (filename) => {
      try {
        // Create download URL
        const downloadUrl = `/api/patient/download-export/${filename}`
        
        // Create a temporary link and trigger download
        const link = document.createElement('a')
        link.href = downloadUrl
        link.download = filename
        link.style.display = 'none'
        
        // Add authorization header by creating a blob from fetch
        const token = localStorage.getItem('access_token')
        const response = await fetch(downloadUrl, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        
        if (response.ok) {
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          link.href = url
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

    onMounted(() => {
      fetchProfile()
    })

    return {
      loading,
      editMode,
      exportLoading,
      profile,
      stats,
      form,
      updateProfile,
      cancelEdit,
      formatDate,
      calculateAge,
      exportTreatments,
      downloadFile
    }
  }
}
</script>
