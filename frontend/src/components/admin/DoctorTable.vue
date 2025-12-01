<template>
  <DataTable
    :columns="columns"
    :data="doctors"
    empty-message="No doctors found"
  >
    <template #body="{ data }">
      <tr v-for="doctor in data" :key="doctor.id">
        <td>{{ doctor.id }}</td>
        <td>{{ doctor.name }}</td>
        <td>{{ doctor.specialization }}</td>
        <td>{{ doctor.department_name || 'N/A' }}</td>
        <td>{{ doctor.phone || 'N/A' }}</td>
        <td>{{ doctor.years_of_experience }} years</td>
        <td>
          <span :class="doctor.is_active ? 'badge bg-success' : 'badge bg-secondary'">
            {{ doctor.is_active ? 'Active' : 'Inactive' }}
          </span>
        </td>
        <td>
          <button @click="$emit('edit', doctor)" class="btn btn-sm btn-secondary me-1">
            <i class="bi bi-pencil"></i>
          </button>
          <button @click="$emit('delete', doctor.id)" class="btn btn-sm btn-danger">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      </tr>
    </template>
  </DataTable>
</template>

<script>
import DataTable from '@/components/common/DataTable.vue'

export default {
  name: 'DoctorTable',
  components: {
    DataTable
  },
  props: {
    doctors: {
      type: Array,
      default: () => []
    }
  },
  emits: ['edit', 'delete'],
  data() {
    return {
      columns: [
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Name' },
        { key: 'specialization', label: 'Specialization' },
        { key: 'department', label: 'Department' },
        { key: 'phone', label: 'Phone' },
        { key: 'experience', label: 'Experience' },
        { key: 'status', label: 'Status' },
        { key: 'actions', label: 'Actions' }
      ]
    }
  }
}
</script>
