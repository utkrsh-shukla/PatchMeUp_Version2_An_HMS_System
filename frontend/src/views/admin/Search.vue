<template>
  <div class="container my-5">
    <h2 class="mb-4"><i class="bi bi-search"></i> Search Patients & Doctors</h2>

    <!-- Search Form -->
    <div class="card mb-4">
      <div class="card-body">
        <form @submit.prevent="performSearch">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Search</label>
              <input 
                v-model="query" 
                class="form-control" 
                placeholder="Search by name, email, or specialization"
                required
              >
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Search In</label>
              <select v-model="searchType" class="form-select">
                <option value="all">All</option>
                <option value="doctor">Doctors</option>
                <option value="patient">Patients</option>
              </select>
            </div>
            <div class="col-md-2 mb-3">
              <label class="form-label">&nbsp;</label>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Search
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary"></div>
      <p class="mt-2">Searching...</p>
    </div>

    <!-- Results -->
    <template v-else-if="searched">
      <!-- Doctors Results -->
      <div v-if="results.doctors && results.doctors.length > 0" class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0"><i class="bi bi-person-badge"></i> Doctors ({{ results.doctors.length }})</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Specialization</th>
                  <th>Department</th>
                  <th>Phone</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="doctor in results.doctors" :key="doctor.id">
                  <td>{{ doctor.name }}</td>
                  <td>{{ doctor.specialization }}</td>
                  <td>{{ doctor.department_name || 'N/A' }}</td>
                  <td>{{ doctor.phone || 'N/A' }}</td>
                  <td>{{ doctor.email }}</td>
                  <td>
                    <span :class="doctor.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                      {{ doctor.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <button 
                      @click="toggleStatus(doctor.user_id)" 
                      class="btn btn-sm btn-outline-warning"
                      :disabled="toggling"
                    >
                      {{ doctor.is_active ? 'Deactivate' : 'Activate' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Patients Results -->
      <div v-if="results.patients && results.patients.length > 0" class="card mb-4">
        <div class="card-header">
          <h5 class="mb-0"><i class="bi bi-person-hearts"></i> Patients ({{ results.patients.length }})</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Blood Group</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in results.patients" :key="patient.id">
                  <td>{{ patient.name }}</td>
                  <td>{{ patient.email }}</td>
                  <td>{{ patient.phone || 'N/A' }}</td>
                  <td>{{ patient.blood_group || 'N/A' }}</td>
                  <td>
                    <span :class="patient.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                      {{ patient.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group btn-group-sm">
                      <router-link 
                        :to="`/admin/patients/${patient.id}/history`" 
                        class="btn btn-outline-info"
                        title="View History"
                      >
                        <i class="bi bi-clock-history"></i>
                      </router-link>
                      <button 
                        @click="toggleStatus(patient.user_id)" 
                        class="btn btn-outline-warning"
                        :disabled="toggling"
                      >
                        {{ patient.is_active ? 'Deactivate' : 'Activate' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- No Results Message -->
      <div v-if="(!results.doctors || results.doctors.length === 0) && (!results.patients || results.patients.length === 0)" class="card">
        <div class="card-body text-center py-5">
          <i class="bi bi-search fs-1 text-muted"></i>
          <h5 class="mt-3">No results found for "{{ query }}"</h5>
          <p class="text-muted">Try searching with different keywords or check the spelling.</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref } from 'vue'
import adminAPI from '@/api/admin'

export default {
  name: 'AdminSearch',
  setup() {
    const query = ref('')
    const searchType = ref('all')
    const results = ref({ doctors: [], patients: [] })
    const searched = ref(false)
    const loading = ref(false)
    const toggling = ref(false)

    const performSearch = async () => {
      if (!query.value.trim()) {
        alert('Please enter a search term')
        return
      }

      try {
        loading.value = true
        const response = await adminAPI.search(query.value, searchType.value)
        results.value = response.data.data
        searched.value = true
      } catch (error) {
        console.error('Error searching:', error)
        alert('Error performing search')
      } finally {
        loading.value = false
      }
    }

    const toggleStatus = async (userId) => {
      if (!confirm('Are you sure you want to change this user\'s status?')) {
        return
      }

      try {
        toggling.value = true
        await adminAPI.toggleUserStatus(userId)
        await performSearch() // Refresh results
        alert('User status updated successfully')
      } catch (error) {
        console.error('Error toggling status:', error)
        alert('Error updating user status')
      } finally {
        toggling.value = false
      }
    }

    return {
      query,
      searchType,
      results,
      searched,
      loading,
      toggling,
      performSearch,
      toggleStatus
    }
  }
}
</script>

