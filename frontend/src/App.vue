<template>
  <div v-if="!loading" id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
      <span v-if="isAuthenticated"><router-link to="/sockets">Sockets</router-link> | </span>
      <span><a v-if="isAuthenticated" href="#logout" @click="logout">Logout</a></span>
    </div>
        <transition
          name="fade"
          mode="out-in">
          <router-view :key="$route.path"/>
        </transition>
  </div>
</template>

<script>
import axios from 'axios';
import { USER_REQUEST } from '@/store/actions/user';
import { AUTH_REFRESH } from '@/store/actions/auth';
import { AUTH_LOGOUT } from '@/store/actions/auth'
import { mapGetters } from 'vuex'

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
  },
  created: function () {
    if (this.$store.getters.isAuthenticated) {
      this.$store.dispatch(USER_REQUEST);
      // refresh the token every 4 minutes while the user is logged in
      setInterval(() => { this.$store.dispatch(AUTH_REFRESH); }, 1000 * 60 * 4);
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch(AUTH_LOGOUT).then(() => {
        this.$router.push('/login')
      });
      location.reload();
    },

  },
  computed: {
    ...mapGetters(['getProfile', 'isAuthenticated', 'isProfileLoaded']),
  }
}
</script>

<style lang="scss">
  .fade-enter-active,
  .fade-leave-active {
    transition-duration: 0.15s;
    transition-property: opacity;
    transition-timing-function: ease;
  }

  .fade-enter,
  .fade-leave-active {
    opacity: 0
  }


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
