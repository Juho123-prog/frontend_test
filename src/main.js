import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'vuefinder/dist/style.css'
import VueFinder from 'vuefinder'

const app = createApp(App)

// 🔥 vuefinder 전역 등록
app.use(VueFinder)

// 🔥 router 등록
app.use(router)

app.mount('#app')