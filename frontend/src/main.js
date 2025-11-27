import './assets/main.css'   

import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import { createPinia } from 'pinia'

const app = createApp(App);
const pinia = createPinia()

app.use(pinia)
app.use(router); // register router

// Initialize auth store to restore session
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
authStore.initialize()


app.mount('#app');
