import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import filters from './filters';
import VueNativeSock from 'vue-native-websocket'


// Vue.use(new VueSocketIO({
//     debug: true,
//     connection: process.env.VUE_APP_SOCKET_URL || 'http://localhost',
//     vuex: {
//         store,
//         actionPrefix: 'SOCKET_',
//         mutationPrefix: 'SOCKET_'
//     },
//     options: { path: "/ws/chat/myroom/" } //Optional options
// }))

// Vue.use(VueNativeSock, '//localhost/ws/chat/oij/', {  format: 'json' })
Vue.use(VueNativeSock, 'ws://localhost/ws/chat/oijrfe/', { format: 'json' })

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
