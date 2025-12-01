<template>
  <form @submit.prevent="handleSubmit">
    <div class="row mb-3">
      <div class="col-md-6">
        <strong>Patient:</strong> {{ appointment?.patient_name }}
      </div>
      <div class="col-md-6">
        <strong>Date:</strong> {{ formatDate(appointment?.date) }} at {{ formatTime(appointment?.time) }}
      </div>
    </div>

    <div class="mb-3">
      <label for="diagnosis" class="form-label">Diagnosis *</label>
      <textarea
        id="diagnosis"
        v-model="form.diagnosis"
        class="form-control"
        rows="3"
        placeholder="Enter diagnosis..."
        required
      ></textarea>
    </div>

    <div class="mb-3">
      <label for="prescription" class="form-label">Prescription</label>
      <textarea
        id="prescription"
        v-model="form.prescription"
        class="form-control"
        rows="4"
        placeholder="Enter prescription details..."
      ></textarea>
    </div>

    <div class="mb-3">
      <label for="notes" class="form-label">Additional Notes</label>
      <textarea
        id="notes"
        v-model="form.notes"
        class="form-control"
        rows="3"
        placeholder="Any additional notes..."
      ></textarea>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" @click="$emit('cancel')" class="btn btn-secondary">
        Cancel
      </button>
      <button type="submit" class="btn btn-success">
        <i class="bi bi-check-circle"></i> {{ isEdit ? 'Update Treatment' : 'Add Treatment & Complete' }}
      </button>
    </div>
  </form>
</template>

<script>
import { ref, watch } from 'vue'
import { useFormatting } from '@/composables/useFormatting'

export default {
  name: 'TreatmentForm',
  props: {
    appointment: { type: Object, default: null },
    isEdit: { type: Boolean, default: false }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const { formatDate, formatTime } = useFormatting()
    const form = ref({ diagnosis: '', prescription: '', notes: '' })

    const handleSubmit = () => {
      if (!form.value.diagnosis.trim()) {
        alert('Diagnosis is required')
        return
      }
      emit('submit', {
        diagnosis: form.value.diagnosis.trim(),
        prescription: form.value.prescription.trim() || null,
        notes: form.value.notes.trim() || null
      })
    }

    watch(() => props.appointment, () => {
      if (props.isEdit && props.appointment?.treatment) {
        // Pre-fill form with existing treatment data
        form.value = {
          diagnosis: props.appointment.treatment.diagnosis || '',
          prescription: props.appointment.treatment.prescription || '',
          notes: props.appointment.treatment.notes || ''
        }
      } else {
        form.value = { diagnosis: '', prescription: '', notes: '' }
      }
    }, { immediate: true })

    return { form, handleSubmit, formatDate, formatTime, isEdit: props.isEdit }
  }
}
</script>