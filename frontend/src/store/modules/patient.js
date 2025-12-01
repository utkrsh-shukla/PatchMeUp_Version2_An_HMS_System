import patientAPI from '@/api/patient'

export default {
    namespaced: true,

    state: {
        stats: null,
        departments: [],
        doctors: [],
        appointments: [],
        profile: null,
        loading: false,
        error: null
    },

    mutations: {
        SET_STATS(state, stats) {
            state.stats = stats
        },

        SET_DEPARTMENTS(state, departments) {
            state.departments = departments
        },

        SET_DOCTORS(state, doctors) {
            state.doctors = doctors
        },

        SET_APPOINTMENTS(state, appointments) {
            state.appointments = appointments
        },

        SET_PROFILE(state, profile) {
            state.profile = profile
        },

        SET_LOADING(state, loading) {
            state.loading = loading
        },

        SET_ERROR(state, error) {
            state.error = error
        }
    },

    actions: {
        async fetchStats({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await patientAPI.getStats()
                commit('SET_STATS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchDepartments({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await patientAPI.getDepartments()
                commit('SET_DEPARTMENTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchDoctors({ commit }, departmentId = null) {
            try {
                commit('SET_LOADING', true)
                const response = await patientAPI.getDoctors(departmentId)
                commit('SET_DOCTORS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchUpcomingAppointments({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await patientAPI.getUpcomingAppointments()
                commit('SET_APPOINTMENTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchProfile({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await patientAPI.getProfile()
                commit('SET_PROFILE', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        }
    }
}
