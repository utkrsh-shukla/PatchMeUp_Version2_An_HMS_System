import { createStore } from 'vuex'
import auth from './modules/auth'
import admin from './modules/admin'
import doctor from './modules/doctor'
import patient from './modules/patient'

export default createStore({
    modules: {
        auth,
        admin,
        doctor,
        patient
    }
})
