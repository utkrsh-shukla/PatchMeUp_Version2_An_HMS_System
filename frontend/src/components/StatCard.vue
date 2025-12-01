<template>
  <div class="stat-card">
    <div class="stat-number">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    value: {
      type: [Number, String],
      required: true
    },
    label: {
      type: String,
      required: true
    }
  }
}
</script>
