// import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from "axios"

const app = createApp(App)
app.config.globalProperties.$http=axios;

app.use(ElementPlus)

app.use(router)

app.mount('#app')
