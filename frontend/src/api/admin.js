import apiClient from './axios'

export default {
    getStats: () => apiClient.get('/admin/stats'),
    getDoctors: () => apiClient.get('/admin/doctors'),
    getDoctor: (id) => apiClient.get(`/admin/doctors/${id}`),
    createDoctor: (data) => apiClient.post('/admin/doctors', data),
    updateDoctor: (id, data) => apiClient.put(`/admin/doctors/${id}`, data),
    deleteDoctor: (id) => apiClient.delete(`/admin/doctors/${id}`),
    getPatients: () => apiClient.get('/admin/patients'),
    getPatient: (id) => apiClient.get(`/admin/patients/${id}`),
    getPatientHistory: (id) => apiClient.get(`/admin/patients/${id}/history`),
    updatePatient: (id, data) => apiClient.put(`/admin/patients/${id}`, data),
    deletePatient: (id) => apiClient.delete(`/admin/patients/${id}`),
    getAppointments: () => apiClient.get('/admin/appointments'),
    getUpcomingAppointments: () => apiClient.get('/admin/appointments/upcoming'),
    search: (query, type = 'all') => apiClient.get('/admin/search', { params: { q: query, type } }),
    getDepartments: () => apiClient.get('/admin/departments'),
    toggleUserStatus: (id) => apiClient.put(`/admin/users/${id}/toggle-status`),
    triggerDailyReminders: () => apiClient.post('/admin/jobs/trigger-reminders'),
    triggerMonthlyReports: () => apiClient.post('/admin/jobs/trigger-reports'),
    getJobStatus: (taskId) => apiClient.get(`/admin/jobs/${taskId}/status`),
    getActiveJobs: () => apiClient.get('/admin/jobs/active')
}
