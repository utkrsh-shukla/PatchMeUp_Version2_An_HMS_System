<template>
  <div class="card">
    <div class="card-header">
      <h5 class="mb-0"><i class="bi bi-hospital"></i> Browse Doctors by Department</h5>
    </div>
    <div class="card-body">
      <div class="row">
        <div v-for="dept in departments" :key="dept.id" class="col-md-4 mb-3">
          <div class="card feature-card h-100">
            <div class="card-body text-center">
              <h5 class="text-danger">{{ dept.name }}</h5>
              <p class="text-muted">{{ dept.description || 'Specialized medical care' }}</p>
              <p><strong>{{ dept.doctor_count || 0 }}</strong> Doctors Available</p>
              <router-link :to="'/patient/doctors?department=' + dept.id" class="btn btn-sm btn-primary">
                View Doctors
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DepartmentGrid',
  props: {
    departments: {
      type: Array,
      default: () => []
    }
  }
}
</script>
