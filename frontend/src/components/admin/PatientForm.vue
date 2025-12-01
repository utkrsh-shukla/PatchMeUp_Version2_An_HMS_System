<template>
  <form @submit.prevent="handleSubmit">
    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Name *</label>
        <input
          type="text"
          class="form-control"
          v-model="formData.name"
          required
        >
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Email *</label>
        <input
          type="email"
          class="form-control"
          v-model="formData.email"
          readonly
        >
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Phone</label>
        <input
          type="tel"
          class="form-control"
          v-model="formData.phone"
        >
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Blood Group</label>
        <select class="form-select" v-model="formData.blood_group">
          <option value="">Select</option>
          <option>A+</option>
          <option>A-</option>
          <option>B+</option>
          <option>B-</option>
          <option>AB+</option>
          <option>AB-</option>
          <option>O+</option>
          <option>O-</option>
        </select>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Date of Birth</label>
        <input
          type="date"
          class="form-control"
          v-model="formData.date_of_birth"
        >
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Gender</label>
        <select class="form-select" v-model="formData.gender">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>
    </div>

    <div class="mb-3">
      <label class="form-label">Address</label>
      <textarea
        class="form-control"
        v-model="formData.address"
        rows="3"
      ></textarea>
    </div>

    <div class="d-flex justify-content-between">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Cancel
      </button>
      <button type="submit" class="btn btn-primary">
        Update Patient
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: 'PatientForm',
  props: {
    patient: {
      type: Object,
      default: null
    }
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      formData: {
        name: '',
        email: '',
        phone: '',
        blood_group: '',
        date_of_birth: '',
        gender: '',
        address: ''
      }
    }
  },
  watch: {
    patient: {
      immediate: true,
      handler(newPatient) {
        if (newPatient) {
          this.formData = {
            name: newPatient.name,
            email: newPatient.email,
            phone: newPatient.phone,
            blood_group: newPatient.blood_group,
            date_of_birth: newPatient.date_of_birth,
            gender: newPatient.gender,
            address: newPatient.address
          }
        }
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', { ...this.formData })
    }
  }
}
</script>
