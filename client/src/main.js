import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueGraph from 'vue-graph'

Vue.config.productionTip = false
Vue.use(VueGraph)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

