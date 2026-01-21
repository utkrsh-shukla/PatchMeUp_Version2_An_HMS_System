import axios from 'axios'
import router from '../router'

// Create axios instance
const apiClient = axios.create({
    
    baseURL: 'https://patchmeup-version2-an-hms-system.onrender.com/api',
    headers: {
        'Content-Type': 'application/json'
    }
})

//Request interceptor to add JWT token
apiClient.interceptors.request.use(
    config => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        // If 401 and has refresh token, try to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
                try {
                    const { data } = await axios.post('/api/auth/refresh', {}, {
                        headers: { Authorization: `Bearer ${refreshToken}` }
                    })

                    localStorage.setItem('access_token', data.data.access_token)
                    originalRequest.headers.Authorization = `Bearer ${data.data.access_token}`

                    return apiClient(originalRequest)
                } catch (refreshError) {
                    // Refresh failed, logout
                    localStorage.removeItem('access_token')
                    localStorage.removeItem('refresh_token')
                    localStorage.removeItem('user')
                    router.push('/login')
                    return Promise.reject(refreshError)
                }
            } else {
                // No refresh token, redirect to login
                router.push('/login')
            }
        }

        return Promise.reject(error)
    }
)

export default apiClient
