import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import filters from './filters';
import VueNativeSock from 'vue-native-websocket'

const protocol = process.env.VUE_APP_WS_PROTOCOL;
const host = process.env.VUE_APP_BASE_HOST;

Vue.use(VueNativeSock, `${protocol}${host}/ws/chat/_/`, {
  connectManually: true,
  format: 'json'
});

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
