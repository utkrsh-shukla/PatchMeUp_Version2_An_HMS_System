import authAPI from '@/api/auth'

export default {
    namespaced: true,

    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        accessToken: localStorage.getItem('access_token') || null,
        refreshToken: localStorage.getItem('refresh_token') || null,
        loading: false,
        error: null
    },

    getters: {
        isAuthenticated: state => !!state.accessToken,
        currentUser: state => state.user,
        userRole: state => state.user?.role || null,
        isAdmin: state => state.user?.role === 'admin',
        isDoctor: state => state.user?.role === 'doctor',
        isPatient: state => state.user?.role === 'patient'
    },

    mutations: {
        SET_USER(state, user) {
            state.user = user
            if (user) {
                localStorage.setItem('user', JSON.stringify(user))
            } else {
                localStorage.removeItem('user')
            }
        },

        SET_TOKENS(state, { accessToken, refreshToken }) {
            state.accessToken = accessToken
            state.refreshToken = refreshToken
            localStorage.setItem('access_token', accessToken)
            if (refreshToken) {
                localStorage.setItem('refresh_token', refreshToken)
            }
        },

        CLEAR_AUTH(state) {
            state.user = null
            state.accessToken = null
            state.refreshToken = null
            localStorage.removeItem('user')
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
        },

        SET_LOADING(state, loading) {
            state.loading = loading
        },

        SET_ERROR(state, error) {
            state.error = error
        }
    },

    actions: {
        async login({ commit }, credentials) {
            try {
                commit('SET_LOADING', true)
                commit('SET_ERROR', null)

                const response = await authAPI.login(credentials)
                const { access_token, refresh_token, user } = response.data.data

                commit('SET_TOKENS', {
                    accessToken: access_token,
                    refreshToken: refresh_token
                })
                commit('SET_USER', user)

                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Login failed'
                commit('SET_ERROR', message)
                throw new Error(message)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async register({ commit }, data) {
            try {
                commit('SET_LOADING', true)
                commit('SET_ERROR', null)

                const response = await authAPI.register(data)
                return response.data
            } catch (error) {
                const message = error.response?.data?.error || 'Registration failed'
                commit('SET_ERROR', message)
                throw new Error(message)
            } finally {
                commit('SET_LOADING', false)
            }
        },

        async getCurrentUser({ commit }) {
            try {
                const response = await authAPI.getCurrentUser()
                commit('SET_USER', response.data.data)
                return response.data.data
            } catch (error) {
                commit('CLEAR_AUTH')
                throw error
            }
        },

        logout({ commit }) {
            commit('CLEAR_AUTH')
        }
    }
}
