import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import filters from './filters';
import VueNativeSock from 'vue-native-websocket'

Vue.use(VueNativeSock, 'ws://localhost/ws/chat/name/', {
  connectManually: true,
  format: 'json'
})

// register all filters globally
for (let name in filters) {
    Vue.filter(name, filters[name]);
}
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
