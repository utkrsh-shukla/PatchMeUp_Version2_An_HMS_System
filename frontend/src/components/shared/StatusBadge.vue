<template>
  <span :class="badgeClass">{{ displayStatus }}</span>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'StatusBadge',
  props: {
    status: {
      type: String,
      required: true,
      validator: (value) => ['booked', 'completed', 'cancelled', 'rescheduled'].includes(value)
    }
  },
  setup(props) {
    const badgeClass = computed(() => `badge badge-${props.status}`)
    const displayStatus = computed(() => props.status.charAt(0).toUpperCase() + props.status.slice(1))
    
    return { badgeClass, displayStatus }
  }
}
</script>
