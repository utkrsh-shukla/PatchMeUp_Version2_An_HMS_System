import doctorAPI from '@/api/doctor'

export default {
    namespaced: true,

    state: {
        stats: null,
        todayAppointments: [],
        upcomingAppointments: [],
        availability: null,
        loading: false,
        error: null
    },

    mutations: {
        SET_STATS(state, stats) {
            state.stats = stats
        },

        SET_TODAY_APPOINTMENTS(state, appointments) {
            state.todayAppointments = appointments
        },

        SET_UPCOMING_APPOINTMENTS(state, appointments) {
            state.upcomingAppointments = appointments
        },

        SET_AVAILABILITY(state, availability) {
            state.availability = availability
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
                const response = await doctorAPI.getStats()
                commit('SET_STATS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchTodayAppointments({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await doctorAPI.getTodayAppointments()
                commit('SET_TODAY_APPOINTMENTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchUpcomingAppointments({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await doctorAPI.getUpcomingAppointments()
                commit('SET_UPCOMING_APPOINTMENTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchAvailability({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await doctorAPI.getAvailability()
                commit('SET_AVAILABILITY', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        }
    }
}
