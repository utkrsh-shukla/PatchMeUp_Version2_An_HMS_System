<template>
  <footer class="footer mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <h5>About PatchMeUp</h5>
          <p>PatchMeUp Hospital's HMS, A comprehensive hospital management system for efficient healthcare delivery. Developed by Yours Truly Utkarsh Shukla (utkrsh313@gmail.com)</p>
        </div>
        <div class="col-md-4">
          <h5>Quick Links</h5>
          <ul class="list-unstyled">
            <li><router-link to="/">Home</router-link></li>
            <li v-if="!isAuthenticated"><router-link to="/login">Login</router-link></li>
            <li v-if="!isAuthenticated"><router-link to="/register">Register</router-link></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h5>Contact Information</h5>
          <p><i class="bi bi-telephone"></i> Call us: +91 1212121212</p>
          <p><i class="bi bi-envelope"></i> Email: something@patchmeup.com</p>
          <p><i class="bi bi-geo-alt"></i> Address: Universe 7 Planet Namek</p>
        </div>
      </div>
      <hr>
      <p class="text-center mb-0">&copy; 2025 PatchMeUp Hospital. All Rights Reserved.</p>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Footer',
  setup() {
    const store = useStore()
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    
    return {
      isAuthenticated
    }
  }
}
</script>

