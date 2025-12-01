<template>
  <PageLayout title="Manage Patients" icon="bi bi-person-hearts">
    <LoadingSpinner v-if="loading" />

    <PatientTable
      v-else
      :patients="patients"
      @view-history="viewHistory"
      @edit="openEditModal"
      @delete="handleDelete"
    />

    <FormModal
      :show="showModal"
      title="Edit Patient"
      size="lg"
      @close="closeModal"
    >
      <PatientForm
        :patient="selectedPatient"
        @submit="handleSave"
        @cancel="closeModal"
      />
    </FormModal>
  </PageLayout>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageLayout from '@/components/layout/PageLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import PatientTable from '@/components/admin/PatientTable.vue'
import PatientForm from '@/components/admin/PatientForm.vue'
import FormModal from '@/components/common/FormModal.vue'
import adminAPI from '@/api/admin'

export default {
  name: 'AdminPatients',
  components: {
    PageLayout,
    LoadingSpinner,
    PatientTable,
    PatientForm,
    FormModal
  },
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const patients = ref([])
    const showModal = ref(false)
    const selectedPatient = ref(null)

    const fetchPatients = async () => {
      try {
        const response = await adminAPI.getPatients()
        patients.value = response.data.data
      } catch (error) {
        console.error('Error fetching patients:', error)
      } finally {
        loading.value = false
      }
    }

    const viewHistory = (id) => {
      router.push(`/admin/patients/${id}/history`)
    }

    const openEditModal = (patient) => {
      selectedPatient.value = patient
      showModal.value = true
    }

    const handleSave = async (patientData) => {
      try {
        await adminAPI.updatePatient(selectedPatient.value.id, patientData)
        await fetchPatients()
        closeModal()
      } catch (error) {
        console.error('Error saving patient:', error)
        alert(error.response?.data?.message || 'Error saving patient')
      }
    }

    const handleDelete = async (id) => {
      if (confirm('Are you sure you want to deactivate this patient?')) {
        try {
          await adminAPI.toggleUserStatus(id)
          await fetchPatients()
        } catch (error) {
          console.error('Error deleting patient:', error)
        }
      }
    }

    const closeModal = () => {
      showModal.value = false
      selectedPatient.value = null
    }

    onMounted(() => {
      fetchPatients()
    })

    return {
      loading,
      patients,
      showModal,
      selectedPatient,
      viewHistory,
      openEditModal,
      handleSave,
      handleDelete,
      closeModal
    }
  }
}
</script>

