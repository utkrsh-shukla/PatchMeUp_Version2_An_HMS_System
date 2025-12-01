<template>
  <div class="card mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0"><i class="bi bi-person-hearts"></i> Registered Patients</h5>
      <router-link to="/admin/patients" class="btn btn-sm btn-primary">View All</router-link>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Phone</th>
              <th>Blood Group</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in patients" :key="patient.id">
              <td>{{ patient.id }}</td>
              <td>{{ patient.name }}</td>
              <td>{{ patient.phone || 'N/A' }}</td>
              <td>{{ patient.blood_group || 'N/A' }}</td>
              <td>
                <span :class="patient.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ patient.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
            </tr>
            <tr v-if="!patients || patients.length === 0">
              <td colspan="5" class="text-center text-muted">No patients registered yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PatientsSection',
  props: {
    patients: {
      type: Array,
      default: () => []
    }
  }
}
</script>
