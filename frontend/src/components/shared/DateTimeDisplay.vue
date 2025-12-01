<template>
  <span>{{ displayValue }}</span>
</template>

<script>
import { computed } from 'vue'
import { useFormatting } from '@/composables/useFormatting'

export default {
  name: 'DateTimeDisplay',
  props: {
    date: { type: String, default: null },
    time: { type: String, default: null },
    format: { type: String, default: 'date', validator: (value) => ['date', 'time', 'datetime'].includes(value) }
  },
  setup(props) {
    const { formatDate, formatTime, formatDateTime } = useFormatting()
    
    const displayValue = computed(() => {
      if (props.format === 'date') return formatDate(props.date)
      if (props.format === 'time') return formatTime(props.time)
      return formatDateTime(props.date, props.time)
    })
    
    return { displayValue }
  }
}
</script>
