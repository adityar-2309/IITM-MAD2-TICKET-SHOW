import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './axios'
import store from './store/store'
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
import './registerServiceWorker'





createApp(App).use(router).use(store).mount('#app')
