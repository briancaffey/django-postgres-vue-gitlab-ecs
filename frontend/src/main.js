import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import filters from './filters';

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
