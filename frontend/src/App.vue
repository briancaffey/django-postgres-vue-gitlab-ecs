<template>
  <div id="app">
    <div class="nav">
      <navigation />
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
import Navigation from '@/views/Navigation.vue';

export default {

  components: { Navigation },

  created: function () {
    if (this.$store.getters.isAuthenticated) {
      this.$store.dispatch(USER_REQUEST);
      // refresh the token every 4 minutes while the user is logged in
      setInterval(() => { this.$store.dispatch(AUTH_REFRESH); }, 1000 * 60 * 4);
    }
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

.nav {
  padding: 15px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
