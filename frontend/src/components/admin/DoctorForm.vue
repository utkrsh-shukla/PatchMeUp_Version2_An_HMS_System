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
          :readonly="isEdit"
          required
        >
      </div>
    </div>

    <div v-if="!isEdit" class="mb-3">
      <label class="form-label">Password *</label>
      <input
        type="password"
        class="form-control"
        v-model="formData.password"
        :required="!isEdit"
      >
    </div>

    <div class="row">
      <div class="col-md-6 mb-3">
        <label class="form-label">Specialization *</label>
        <input
          type="text"
          class="form-control"
          v-model="formData.specialization"
          required
        >
      </div>
      <div class="col-md-6 mb-3">
        <label class="form-label">Department *</label>
        <select class="form-select" v-model="formData.department_id" required>
          <option value="">Select Department</option>
          <option
            v-for="dept in departments"
            :key="dept.id"
            :value="dept.id"
          >
            {{ dept.name }}
          </option>
        </select>
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
        <label class="form-label">Years of Experience *</label>
        <input
          type="number"
          class="form-control"
          v-model="formData.years_of_experience"
          min="0"
          required
        >
      </div>
    </div>

    <div class="d-flex justify-content-between">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">
        Cancel
      </button>
      <button type="submit" class="btn btn-primary">
        {{ isEdit ? 'Update' : 'Add' }} Doctor
      </button>
    </div>
  </form>
</template>

<script>
export default {
  name: 'DoctorForm',
  props: {
    doctor: {
      type: Object,
      default: null
    },
    departments: {
      type: Array,
      default: () => []
    }
  },
  emits: ['submit', 'cancel'],
  data() {
    return {
      formData: {
        name: '',
        email: '',
        password: '',
        specialization: '',
        department_id: '',
        phone: '',
        years_of_experience: 0
      }
    }
  },
  computed: {
    isEdit() {
      return this.doctor !== null
    }
  },
  watch: {
    doctor: {
      immediate: true,
      handler(newDoctor) {
        if (newDoctor) {
          this.formData = {
            name: newDoctor.name,
            email: newDoctor.email,
            specialization: newDoctor.specialization,
            department_id: newDoctor.department_id,
            phone: newDoctor.phone,
            years_of_experience: newDoctor.years_of_experience
          }
        } else {
          this.resetForm()
        }
      }
    }
  },
  methods: {
    handleSubmit() {
      this.$emit('submit', { ...this.formData })
    },
    resetForm() {
      this.formData = {
        name: '',
        email: '',
        password: '',
        specialization: '',
        department_id: '',
        phone: '',
        years_of_experience: 0
      }
    }
  }
}
</script>
