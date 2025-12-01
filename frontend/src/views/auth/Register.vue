<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-danger text-white">
            <h4 class="mb-0">Patient Registration</h4>
          </div>
          <div class="card-body p-4">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <div v-if="success" class="alert alert-success" role="alert">
              Registration successful! Please <router-link to="/login">login</router-link>.
            </div>
            
            <form @submit.prevent="handleRegister" v-if="!success">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="name" class="form-label">Full Name *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="name"
                    v-model="formData.name" 
                    required
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email *</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email"
                    v-model="formData.email" 
                    required
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="password" class="form-label">Password *</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="password"
                    v-model="formData.password" 
                    required
                    minlength="6"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="phone" class="form-label">Phone</label>
                  <input 
                    type="tel" 
                    class="form-control" 
                    id="phone"
                    v-model="formData.phone"
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="dob" class="form-label">Date of Birth</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="dob"
                    v-model="formData.date_of_birth"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="blood_group" class="form-label">Blood Group</label>
                  <select class="form-select" id="blood_group" v-model="formData.blood_group">
                    <option value="">Select Blood Group</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea 
                  class="form-control" 
                  id="address"
                  v-model="formData.address"
                  rows="2"
                ></textarea>
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Registering...' : 'Register' }}
              </button>
            </form>
            
            <hr v-if="!success">
            <p class="text-center mb-0" v-if="!success">
              Already have an account? 
              <router-link to="/login">Login</router-link>
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

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    
    const formData = ref({
      name: '',
      email: '',
      password: '',
      phone: '',
      date_of_birth: '',
      blood_group: '',
      address: ''
    })
    
    const loading = computed(() => store.state.auth.loading)
    const error = ref(null)
    const success = ref(false)
    
    const handleRegister = async () => {
      error.value = null
      try {
        await store.dispatch('auth/register', formData.value)
        success.value = true
      } catch (err) {
        error.value = err.message
      }
    }
    
    return {
      formData,
      loading,
      error,
      success,
      handleRegister
    }
  }
}
</script>
