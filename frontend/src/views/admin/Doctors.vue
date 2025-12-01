<template>
  <PageLayout title="Manage Doctors" icon="bi bi-people">
    <template #header-actions>
      <button @click="openAddModal" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Add New Doctor
      </button>
    </template>

    <LoadingSpinner v-if="loading" />
    
    <DoctorTable
      v-else
      :doctors="doctors"
      @edit="openEditModal"
      @delete="handleDelete"
    />

    <FormModal
      :show="showModal"
      :title="selectedDoctor ? 'Edit Doctor' : 'Add New Doctor'"
      size="lg"
      @close="closeModal"
    >
      <DoctorForm
        :doctor="selectedDoctor"
        :departments="departments"
        @submit="handleSave"
        @cancel="closeModal"
      />
    </FormModal>
  </PageLayout>
</template>

<script>
import { ref, onMounted } from 'vue'
import PageLayout from '@/components/layout/PageLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import DoctorTable from '@/components/admin/DoctorTable.vue'
import DoctorForm from '@/components/admin/DoctorForm.vue'
import FormModal from '@/components/common/FormModal.vue'
import adminAPI from '@/api/admin'
import { useStore } from 'vuex'

export default {
  name: 'AdminDoctors',
  components: {
    PageLayout,
    LoadingSpinner,
    DoctorTable,
    DoctorForm,
    FormModal
  },
  setup() {
    const store = useStore()
    const loading = ref(true)
    const doctors = ref([])
    const departments = ref([])
    const showModal = ref(false)
    const selectedDoctor = ref(null)

    const fetchDoctors = async () => {
      try {
        const response = await adminAPI.getDoctors()
        doctors.value = response.data.data
      } catch (error) {
        console.error('Error fetching doctors:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchDepartments = async () => {
      try {
        const response = await adminAPI.getDepartments()
        departments.value = response.data.data
      } catch (error) {
        console.error('Error fetching departments:', error)
      }
    }

    const openAddModal = () => {
      selectedDoctor.value = null
      showModal.value = true
    }

    const openEditModal = (doctor) => {
      selectedDoctor.value = doctor
      showModal.value = true
    }

    const handleSave = async (doctorData) => {
      try {
        if (selectedDoctor.value) {
          await adminAPI.updateDoctor(selectedDoctor.value.id, doctorData)
        } else {
          await adminAPI.createDoctor(doctorData)
        }
        await fetchDoctors()
        closeModal()
      } catch (error) {
        console.error('Error saving doctor:', error)
        alert(error.response?.data?.message || 'Error saving doctor')
      }
    }

    const handleDelete = async (id) => {
      if (confirm('Are you sure you want to deactivate this doctor?')) {
        try {
          await adminAPI.toggleUserStatus(id)
          await fetchDoctors()
        } catch (error) {
          console.error('Error deleting doctor:', error)
        }
      }
    }

    const closeModal = () => {
      showModal.value = false
      selectedDoctor.value = null
    }

    onMounted(() => {
      fetchDoctors()
      fetchDepartments()
    })

    return {
      loading,
      doctors,
      departments,
      showModal,
      selectedDoctor,
      openAddModal,
      openEditModal,
      handleSave,
      handleDelete,
      closeModal
    }
  }
}
</script>

