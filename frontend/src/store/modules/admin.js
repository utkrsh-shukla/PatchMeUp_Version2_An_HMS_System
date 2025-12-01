import adminAPI from '@/api/admin'

export default {
    namespaced: true,

    state: {
        stats: null,
        doctors: [],
        patients: [],
        appointments: [],
        searchResults: null,
        loading: false,
        error: null
    },

    mutations: {
        SET_STATS(state, stats) {
            state.stats = stats
        },

        SET_DOCTORS(state, doctors) {
            state.doctors = doctors
        },

        SET_PATIENTS(state, patients) {
            state.patients = patients
        },

        SET_APPOINTMENTS(state, appointments) {
            state.appointments = appointments
        },

        SET_SEARCH_RESULTS(state, results) {
            state.searchResults = results
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
                const response = await adminAPI.getStats()
                commit('SET_STATS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchDoctors({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await adminAPI.getDoctors()
                commit('SET_DOCTORS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async fetchPatients({ commit }) {
            try {
                commit('SET_LOADING', true)
                const response = await adminAPI.getPatients()
                commit('SET_PATIENTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async search({ commit }, { query, type }) {
            try {
                commit('SET_LOADING', true)
                const response = await adminAPI.search(query, type)
                commit('SET_SEARCH_RESULTS', response.data.data)
            } catch (error) {
                commit('SET_ERROR', error.response?.data?.error)
            } finally {
                commit('SET_LOADING', false)
            }
        }
    }
}
