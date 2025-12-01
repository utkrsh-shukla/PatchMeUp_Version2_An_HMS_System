import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Import custom CSS and JS
import './assets/main.css'
import './assets/main.js'

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
