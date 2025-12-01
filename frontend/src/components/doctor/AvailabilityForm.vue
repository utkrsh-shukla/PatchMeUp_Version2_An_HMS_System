<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label class="form-label">Day of Week *</label>
      <select v-model="formData.day_of_week" class="form-select" required>
        <option value="">Select Day</option>
        <option value="0">Monday</option>
        <option value="1">Tuesday</option>
        <option value="2">Wednesday</option>
        <option value="3">Thursday</option>
        <option value="4">Friday</option>
        <option value="5">Saturday</option>
        <option value="6">Sunday</option>
      </select>
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Start Time *</label>
        <input
          type="time"
          v-model="formData.start_time"
          class="form-control"
          required
        >
      </div>

      <div class="col-md-6 mb-3">
        <label class="form-label">End Time *</label>
        <input
          type="time"
          v-model="formData.end_time"
          class="form-control"
          required
        >
      </div>
    </div>

    <div class="mb-3 form-check">
      <input
        type="checkbox"
        v-model="formData.is_available"
        class="form-check-input"
        id="isAvailable"
      >
      <label class="form-check-label" for="isAvailable">
        Mark as Available
      </label>
    </div>

    <div class="d-flex justify-content-between">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Cancel
      </button>
      <button type="submit" class="btn btn-primary">
        Add Time Slot
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: 'AvailabilityForm',
  emits: ['submit', 'cancel'],
  data() {
    return {
      formData: {
        day_of_week: '',
        start_time: '',
        end_time: '',
        is_available: true
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', { ...this.formData })
      this.resetForm()
    },
    resetForm() {
      this.formData = {
        day_of_week: '',
        start_time: '',
        end_time: '',
        is_available: true
      }
    }
  }
}
</script>
