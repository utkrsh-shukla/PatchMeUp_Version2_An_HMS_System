import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Lazy load components
const Home = () => import('../views/Home.vue')
const Login = () => import('../views/auth/Login.vue')
const Register = () => import('../views/auth/Register.vue')

// Admin views
const AdminDashboard = () => import('../views/admin/Dashboard.vue')
const AdminDoctors = () => import('../views/admin/Doctors.vue')
const AdminPatients = () => import('../views/admin/Patients.vue')
const AdminPatientHistory = () => import('../views/admin/PatientHistory.vue')
const AdminAppointments = () => import('../views/admin/Appointments.vue')
const AdminSearch = () => import('../views/admin/Search.vue')

// Doctor views
const DoctorDashboard = () => import('../views/doctor/Dashboard.vue')
const DoctorAppointments = () => import('../views/doctor/Appointments.vue')
const DoctorAvailability = () => import('../views/doctor/Availability.vue')

// Patient views
const PatientDashboard = () => import('../views/patient/Dashboard.vue')
const PatientDoctors = () => import('../views/patient/Doctors.vue')
const PatientAppointments = () => import('../views/patient/Appointments.vue')
const PatientTreatments = () => import('../views/patient/Treatments.vue')
const PatientProfile = () => import('../views/patient/Profile.vue')

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { guest: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { guest: true }
    },

    // Admin routes
    {
        path: '/admin',
        redirect: '/admin/dashboard',
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/doctors',
        name: 'AdminDoctors',
        component: AdminDoctors,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/patients',
        name: 'AdminPatients',
        component: AdminPatients,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/patients/:id/history',
        name: 'AdminPatientHistory',
        component: AdminPatientHistory,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/appointments',
        name: 'AdminAppointments',
        component: AdminAppointments,
        meta: { requiresAuth: true, role: 'admin' }
    },
    {
        path: '/admin/search',
        name: 'AdminSearch',
        component: AdminSearch,
        meta: { requiresAuth: true, role: 'admin' }
    },

    // Doctor routes
    {
        path: '/doctor',
        redirect: '/doctor/dashboard',
        meta: { requiresAuth: true, role: 'doctor' }
    },
    {
        path: '/doctor/dashboard',
        name: 'DoctorDashboard',
        component: DoctorDashboard,
        meta: { requiresAuth: true, role: 'doctor' }
    },
    {
        path: '/doctor/appointments',
        name: 'DoctorAppointments',
        component: DoctorAppointments,
        meta: { requiresAuth: true, role: 'doctor' }
    },
    {
        path: '/doctor/availability',
        name: 'DoctorAvailability',
        component: DoctorAvailability,
        meta: { requiresAuth: true, role: 'doctor' }
    },

    // Patient routes
    {
        path: '/patient',
        redirect: '/patient/dashboard',
        meta: { requiresAuth: true, role: 'patient' }
    },
    {
        path: '/patient/dashboard',
        name: 'PatientDashboard',
        component: PatientDashboard,
        meta: { requiresAuth: true, role: 'patient' }
    },
    {
        path: '/patient/doctors',
        name: 'PatientDoctors',
        component: PatientDoctors,
        meta: { requiresAuth: true, role: 'patient' }
    },
    {
        path: '/patient/appointments',
        name: 'PatientAppointments',
        component: PatientAppointments,
        meta: { requiresAuth: true, role: 'patient' }
    },
    {
        path: '/patient/treatments',
        name: 'PatientTreatments',
        component: PatientTreatments,
        meta: { requiresAuth: true, role: 'patient' }
    },
    {
        path: '/patient/profile',
        name: 'PatientProfile',
        component: PatientProfile,
        meta: { requiresAuth: true, role: 'patient' }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters['auth/isAuthenticated']
    const userRole = store.getters['auth/userRole']

    // Redirect to appropriate dashboard if authenticated and going to home
    if (to.path === '/' && isAuthenticated) {
        if (userRole === 'admin') {
            return next('/admin/dashboard')
        } else if (userRole === 'doctor') {
            return next('/doctor/dashboard')
        } else if (userRole === 'patient') {
            return next('/patient/dashboard')
        }
    }

    // Check if route requires authentication
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            return next({ name: 'Login', query: { redirect: to.fullPath } })
        }

        // Check role authorization
        if (to.meta.role && to.meta.role !== userRole) {
            return next('/')
        }
    }

    // Redirect authenticated users away from guest pages
    if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
        if (userRole === 'admin') {
            return next('/admin/dashboard')
        } else if (userRole === 'doctor') {
            return next('/doctor/dashboard')
        } else if (userRole === 'patient') {
            return next('/patient/dashboard')
        }
    }

    next()
})

export default router
