import './assets/main.css'
// Import Bootstrap CSS and JS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap'; // if using Bootstrap's JS (modals, tooltips)
import '@fortawesome/fontawesome-free/css/all.css'; // Font Awesome icons

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';


const app = createApp(App)
app.use(router)
app.use(store);
app.mount('#app')
