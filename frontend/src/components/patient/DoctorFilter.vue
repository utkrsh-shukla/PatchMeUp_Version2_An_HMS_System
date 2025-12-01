<template>
  <div class="card mb-4">
    <div class="card-body">
      <form @submit.prevent="handleFilter">
        <div class="row">
          <div class="col-md-10">
            <select v-model="localDepartment" class="form-select">
              <option value="">All Departments</option>
              <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                {{ dept.name }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Filter</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'DoctorFilter',
  props: {
    departments: {
      type: Array,
      default: () => []
    },
    selectedDepartment: {
      type: [String, Number],
      default: ''
    }
  },
  emits: ['filter-change'],
  setup(props, { emit }) {
    const localDepartment = ref(props.selectedDepartment)
    
    watch(() => props.selectedDepartment, (newVal) => {
      localDepartment.value = newVal
    })
    
    const handleFilter = () => {
      emit('filter-change', localDepartment.value)
    }
    
    return {
      localDepartment,
      handleFilter
    }
  }
}
</script>
