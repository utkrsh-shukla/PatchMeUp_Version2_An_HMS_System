<template>
  <div class="row">
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.booked_appointments || 0 }}</div>
        <div class="stat-label">Booked Appointments</div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.completed_appointments || 0 }}</div>
        <div class="stat-label">Completed Appointments</div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-card">
        <div class="stat-number">{{ stats.cancelled_appointments || 0 }}</div>
        <div class="stat-label">Cancelled Appointments</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppointmentStats',
  props: {
    stats: {
      type: Object,
      default: () => ({})
    }
  }
}
</script>
