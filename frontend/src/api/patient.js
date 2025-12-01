import apiClient from './axios'

export default {
    getStats: () => apiClient.get('/patient/stats'),
    getDepartments: () => apiClient.get('/patient/departments'),
    getDoctors: (departmentId = null, searchQuery = null) => {
        const params = {}
        if (departmentId) params.department_id = departmentId
        if (searchQuery) params.search = searchQuery
        return apiClient.get('/patient/doctors', { params })
    },
    getDoctorDetail: (id) => apiClient.get(`/patient/doctors/${id}`),
    bookAppointment: (data) => apiClient.post('/patient/appointments', data),
    getUpcomingAppointments: () => apiClient.get('/patient/appointments/upcoming'),
    getPastAppointments: () => apiClient.get('/patient/appointments/past'),
    cancelAppointment: (id) => apiClient.put(`/patient/appointments/${id}/cancel`),
    rescheduleAppointment: (id, data) => apiClient.put(`/patient/appointments/${id}/reschedule`, data),
    getProfile: () => apiClient.get('/patient/profile'),
    updateProfile: (data) => apiClient.put('/patient/profile', data),
    exportTreatments: () => apiClient.post('/patient/export-treatments'),
    getJobStatus: (taskId) => apiClient.get(`/patient/jobs/${taskId}/status`),
    getTreatmentHistory: () => apiClient.get('/patient/treatments'),
    getTreatmentDetail: (treatmentId) => apiClient.get(`/patient/treatments/${treatmentId}`),
    getBookedSlots: (doctorId, date) => apiClient.get(`/patient/doctors/${doctorId}/booked-slots`, { params: { date } })
}
