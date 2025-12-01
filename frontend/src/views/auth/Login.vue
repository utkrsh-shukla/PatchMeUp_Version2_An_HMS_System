<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Login</h4>
          </div>
          <div class="card-body p-4">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input 
                  type="email" 
                  class="form-control" 
                  id="email"
                  v-model="credentials.email" 
                  required
                >
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="password"
                  v-model="credentials.password" 
                  required
                >
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>
            
            <hr>
            <p class="text-center mb-0">
              Don't have an account? 
              <router-link to="/register">Register as Patient</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const credentials = ref({
      email: '',
      password: ''
    })
    
    const loading = computed(() => store.state.auth.loading)
    const error = ref(null)
    
    const handleLogin = async () => {
      error.value = null
      try {
        await store.dispatch('auth/login', credentials.value)
        
        const role = store.getters['auth/userRole']
        if (role === 'admin') {
          router.push('/admin/dashboard')
        } else if (role === 'doctor') {
          router.push('/doctor/dashboard')
        } else if (role === 'patient') {
          router.push('/patient/dashboard')
        }
      } catch (err) {
        error.value = err.message
      }
    }
    
    return {
      credentials,
      loading,
      error,
      handleLogin
    }
  }
}
</script>
