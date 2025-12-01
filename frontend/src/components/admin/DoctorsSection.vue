<template>
  <div class="card mb-4">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0"><i class="bi bi-person-badge"></i> Registered Doctors</h5>
      <router-link to="/admin/doctors" class="btn btn-sm btn-primary">View All</router-link>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Specialization</th>
              <th>Department</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doctor in doctors" :key="doctor.id">
              <td>{{ doctor.id }}</td>
              <td>{{ doctor.name }}</td>
              <td>{{ doctor.specialization }}</td>
              <td>{{ doctor.department_name || 'N/A' }}</td>
              <td>
                <span :class="doctor.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ doctor.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
            </tr>
            <tr v-if="!doctors || doctors.length === 0">
              <td colspan="5" class="text-center text-muted">No doctors registered yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DoctorsSection',
  props: {
    doctors: {
      type: Array,
      default: () => []
    }
  }
}
</script>
