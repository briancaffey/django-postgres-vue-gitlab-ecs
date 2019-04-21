<template>
  <div v-if="!loading" id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: true
    }
  },
  beforeCreate() {
    // const subdomain = window.location.host.split('.')[0];
    axios.get('/api/verify-domain/').then(() => {
      this.loading = false
    }).catch(() => {
      const redirect_url = process.env.NODE_ENV === 'production'
        ? process.env.VUE_APP_BASE_URL
        : 'http://localhost';
      window.location.replace(redirect_url);
    })
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
