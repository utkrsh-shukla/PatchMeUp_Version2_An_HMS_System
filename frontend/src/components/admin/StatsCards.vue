<template>
  <div class="row mb-4">
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.total_doctors || 0 }}</div>
        <div class="stat-label">Total Doctors</div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.total_patients || 0 }}</div>
        <div class="stat-label">Total Patients</div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.total_appointments || 0 }}</div>
        <div class="stat-label">Total Appointments</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatsCards',
  props: {
    stats: { type: Object, default: () => ({}) }
  }
}
</script>
