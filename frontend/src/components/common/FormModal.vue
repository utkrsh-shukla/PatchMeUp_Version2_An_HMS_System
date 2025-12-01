<template>
  <div v-if="show" class="modal d-block" style="background: rgba(0,0,0,0.5);" @click.self="close">
    <div class="modal-dialog" :class="sizeClass">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div v-if="$slots.footer" class="modal-footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
    }
  },
  computed: {
    sizeClass() {
      return this.size !== 'md' ? `modal-${this.size}` : ''
    }
  },
  methods: {
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal {
  overflow-y: auto;
}

.modal-dialog {
  margin-top: 50px;
  margin-bottom: 50px;
}
</style>
