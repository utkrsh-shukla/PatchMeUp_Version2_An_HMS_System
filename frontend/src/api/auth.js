import apiClient from './axios'

export default {
    register: (data) => apiClient.post('/auth/register', data),
    login: (credentials) => apiClient.post('/auth/login', credentials),
    getCurrentUser: () => apiClient.get('/auth/me'),
    logout: () => apiClient.post('/auth/logout'),
    refresh: () => apiClient.post('/auth/refresh')
}
