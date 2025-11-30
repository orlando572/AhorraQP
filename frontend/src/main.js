/*import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')
*/



import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPersist)


app.use(pinia)
app.use(router)

app.mount('#app')
