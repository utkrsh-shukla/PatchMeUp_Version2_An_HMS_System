import apiClient from './axios'

export default {
    getStats: () => apiClient.get('/doctor/stats'),
    getTodayAppointments: () => apiClient.get('/doctor/appointments/today'),
    getUpcomingAppointments: () => apiClient.get('/doctor/appointments/upcoming'),
    getAllAppointments: () => apiClient.get('/doctor/appointments'),
    completeAppointment: (id) => apiClient.put(`/doctor/appointments/${id}/complete`),
    cancelAppointment: (id) => apiClient.put(`/doctor/appointments/${id}/cancel`),
    addTreatment: (appointmentId, data) => apiClient.post(`/doctor/appointments/${appointmentId}/treatment`, data),
    updateTreatment: (appointmentId, data) => apiClient.put(`/doctor/appointments/${appointmentId}/treatment`, data),
    getPatientHistory: (patientId) => apiClient.get(`/doctor/patients/${patientId}/history`),
    getAvailability: () => apiClient.get('/doctor/availability'),
    addAvailability: (data) => apiClient.post('/doctor/availability', data),
    deleteAvailability: (id) => apiClient.delete(`/doctor/availability/${id}`)
}
