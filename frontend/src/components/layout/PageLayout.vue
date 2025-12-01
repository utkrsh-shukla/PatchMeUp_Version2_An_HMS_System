<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>
        <i v-if="icon" :class="icon"></i>
        {{ title }}
      </h2>
      <slot name="header-actions"></slot>
    </div>
    
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'PageLayout',
  props: {
    title: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: ''
    }
  }
}
</script>
