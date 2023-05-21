import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store' // import the store here
import VTooltip from 'v-tooltip'


const app = createApp(App)
app.use(VTooltip)
app.use(router)
app.use(store) // tell Vue to use the store

app.mount('#app')
