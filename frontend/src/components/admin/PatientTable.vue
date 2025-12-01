<template>
  <div class="card">
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Blood Group</th>
              <th>Date of Birth</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in patients" :key="patient.id">
              <td>{{ patient.id }}</td>
              <td>{{ patient.name }}</td>
              <td>{{ patient.email }}</td>
              <td>{{ patient.phone || 'N/A' }}</td>
              <td>{{ patient.blood_group || 'N/A' }}</td>
              <td>{{ formatDate(patient.date_of_birth) }}</td>
              <td>
                <span :class="patient.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ patient.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button @click="$emit('view-history', patient.id)" class="btn btn-outline-info" title="View History">
                    <i class="bi bi-clock-history"></i>
                  </button>
                  <button @click="$emit('edit', patient)" class="btn btn-outline-warning" title="Edit">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button @click="$emit('delete', patient.id)" class="btn btn-outline-danger" title="Deactivate">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!patients || patients.length === 0">
              <td colspan="8" class="text-center text-muted py-4">
                No patients found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientTable',
  props: {
    patients: {
      type: Array,
      default: () => []
    }
  },
  emits: ['view-history', 'edit', 'delete'],
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return 'N/A'
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }
  }
}
</script>
